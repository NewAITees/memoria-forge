"""Generate a standalone HTML map of the persistent clustering geometry."""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(dot(vector, vector))
    return [value / norm for value in vector] if norm else vector[:]


def internal_similarity(centroid: list[float], size: int) -> float:
    if size < 2:
        return 0.0
    norm_squared = dot(centroid, centroid)
    return max(-1.0, min(1.0, (size * norm_squared - 1.0) / (size - 1)))


def load_clusters(database: Path) -> list[dict[str, Any]]:
    """Load cluster centroids and representative titles without mutating the DB."""
    uri = database.resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    rows = connection.execute(
        """
        SELECT c.cluster_id, c.size, c.centroid, c.page_path, c.paged_size,
               COALESCE((
                   SELECT r.title
                   FROM cluster_members AS m
                   JOIN rss_candidates AS r ON r.url = m.url
                   WHERE m.cluster_id = c.cluster_id
                   ORDER BY m.assigned_at, m.url
                   LIMIT 1
               ), '名称なし')
        FROM clusters AS c
        ORDER BY c.cluster_id
        """
    ).fetchall()
    clusters = [
        {
            "id": int(cluster_id),
            "size": int(size),
            "centroid": json.loads(centroid),
            "page_path": page_path,
            "paged_size": paged_size,
            "title": title,
            "members": [],
            "moc_id": None,
            "moc_title": None,
            "moc_path": None,
            "similarity": internal_similarity(json.loads(centroid), int(size)),
        }
        for cluster_id, size, centroid, page_path, paged_size, title in rows
    ]
    by_id = {cluster["id"]: cluster for cluster in clusters}
    member_rows = connection.execute(
        """
        SELECT m.cluster_id, COALESCE(r.title, m.url)
        FROM cluster_members AS m
        LEFT JOIN rss_candidates AS r ON r.url = m.url
        ORDER BY m.cluster_id, m.assigned_at, m.url
        """
    ).fetchall()
    for cluster_id, title in member_rows:
        members = by_id[int(cluster_id)]["members"]
        if len(members) < 5:
            members.append(title)
    has_mocs = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'moc_members'"
    ).fetchone()
    if has_mocs:
        for cluster_id, moc_id, moc_title, moc_path in connection.execute(
            "SELECT mm.cluster_id, m.moc_id, m.title, m.page_path "
            "FROM moc_members mm JOIN mocs m ON m.moc_id = mm.moc_id"
        ):
            if cluster_id is not None and int(cluster_id) in by_id:
                by_id[int(cluster_id)].update(
                    moc_id=int(moc_id), moc_title=str(moc_title), moc_path=str(moc_path)
                )
    connection.close()
    return clusters


def principal_projection(clusters: list[dict[str, Any]], iterations: int = 15) -> None:
    """Add weighted two-dimensional PCA coordinates to cluster dictionaries."""
    if not clusters:
        return
    vectors = [normalize(cluster["centroid"]) for cluster in clusters]
    weights = [float(cluster["size"]) for cluster in clusters]
    total_weight = sum(weights)
    dimensions = len(vectors[0])
    mean = [
        sum(weight * vector[index] for weight, vector in zip(weights, vectors)) / total_weight
        for index in range(dimensions)
    ]
    centered = [[value - mean[index] for index, value in enumerate(vector)] for vector in vectors]

    axes: list[list[float]] = []
    for seed_index in range(2):
        axis = normalize(
            [math.sin((index + 1) * (seed_index + 1) * 1.61803398875) for index in range(dimensions)]
        )
        for _ in range(iterations):
            scores = [dot(vector, axis) for vector in centered]
            candidate = [
                sum(weight * score * vector[index] for weight, score, vector in zip(weights, scores, centered))
                for index in range(dimensions)
            ]
            for prior in axes:
                overlap = dot(candidate, prior)
                candidate = [value - overlap * prior[index] for index, value in enumerate(candidate)]
            axis = normalize(candidate)
        axes.append(axis)

    for cluster, vector in zip(clusters, centered):
        cluster["x"] = dot(vector, axes[0])
        cluster["y"] = dot(vector, axes[1])


def nearest_relations(clusters: list[dict[str, Any]], minimum: float = 0.72) -> list[dict[str, Any]]:
    """Connect each cluster to its closest peer when cosine similarity is meaningful."""
    vectors = [normalize(cluster["centroid"]) for cluster in clusters]
    relations: dict[tuple[int, int], float] = {}
    for index, vector in enumerate(vectors):
        best_index = -1
        best_similarity = -1.0
        candidates = [other_index for other_index in range(len(vectors)) if other_index != index]
        if "x" in clusters[index]:
            candidates.sort(
                key=lambda other_index: (
                    (clusters[index]["x"] - clusters[other_index]["x"]) ** 2
                    + (clusters[index]["y"] - clusters[other_index]["y"]) ** 2
                )
            )
            candidates = candidates[:16]
        for other_index in candidates:
            other = vectors[other_index]
            similarity = dot(vector, other)
            if similarity > best_similarity:
                best_index = other_index
                best_similarity = similarity
        if best_index >= 0 and best_similarity >= minimum:
            pair = tuple(sorted((clusters[index]["id"], clusters[best_index]["id"])))
            relations[pair] = max(best_similarity, relations.get(pair, -1.0))
    return [
        {"source": source, "target": target, "similarity": similarity}
        for (source, target), similarity in sorted(relations.items())
    ]


def size_histogram(clusters: list[dict[str, Any]]) -> list[dict[str, int | str]]:
    buckets = [(1, 1, "1"), (2, 3, "2–3"), (4, 7, "4–7"), (8, 15, "8–15"),
               (16, 31, "16–31"), (32, 63, "32–63"), (64, 127, "64–127"),
               (128, 10**9, "128以上")]
    return [
        {"label": label, "count": sum(low <= cluster["size"] <= high for cluster in clusters)}
        for low, high, label in buckets
    ]


def render_html(clusters: list[dict[str, Any]], relations: list[dict[str, Any]]) -> str:
    sizes = [cluster["size"] for cluster in clusters]
    similarities = [cluster["similarity"] for cluster in clusters if cluster["size"] > 1]
    summary = {
        "clusters": len(clusters),
        "members": sum(sizes),
        "linked": sum(cluster["page_path"] is not None for cluster in clusters),
        "singletons": Counter(sizes)[1],
        "median_size": sorted(sizes)[len(sizes) // 2] if sizes else 0,
        "mean_similarity": sum(similarities) / len(similarities) if similarities else 0.0,
    }
    public_clusters = [
        {
            key: cluster[key]
            for key in ("id", "size", "page_path", "title", "members", "similarity", "x", "y", "moc_id", "moc_title", "moc_path")
        }
        for cluster in clusters
    ]
    payload = json.dumps(
        {"clusters": public_clusters, "relations": relations, "histogram": size_histogram(clusters), "summary": summary},
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>クラスタ分布マップ</title>
<style>
:root{{--bg:#f7f7f5;--panel:#fff;--text:#202124;--muted:#62666b;--line:#d7d9dc;--blue:#2563eb;--orange:#d97706;--green:#16803c}}
@media(prefers-color-scheme:dark){{:root{{--bg:#17181a;--panel:#222428;--text:#f2f3f5;--muted:#afb3b8;--line:#42464d;--blue:#72a4ff;--orange:#f5ad55;--green:#6dd38c}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:14px system-ui,sans-serif}}
main{{max-width:1500px;margin:auto;padding:24px}} h1{{font-size:24px;margin:0 0 6px}} h2{{font-size:17px;margin:0 0 12px}}
.sub{{color:var(--muted);margin:0 0 18px}} .stats{{display:grid;grid-template-columns:repeat(5,minmax(110px,1fr));gap:10px;margin-bottom:18px}}
.stat,.panel{{background:var(--panel);border:1px solid var(--line);border-radius:10px}} .stat{{padding:12px}} .stat b{{font-size:22px;display:block}}
.stat span{{color:var(--muted)}} .layout{{display:grid;grid-template-columns:minmax(0,3fr) minmax(280px,1fr);gap:14px}}
.panel{{padding:14px}} svg{{display:block;width:100%;height:auto}} .legend{{display:flex;gap:16px;flex-wrap:wrap;color:var(--muted);margin-top:8px}}
.dot{{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:5px}} .controls{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}}
label{{color:var(--muted)}} input{{vertical-align:middle}} .detail{{min-height:52px;color:var(--muted);margin-top:8px}}
circle.cluster{{cursor:pointer;stroke:var(--panel);stroke-width:1}} circle.cluster:focus{{outline:none;stroke:var(--text);stroke-width:2}}
.edge{{stroke:var(--line);stroke-width:1}} .axis{{stroke:var(--line)}} .bar{{fill:var(--blue)}} .bar-label{{fill:var(--text);font-size:12px}}
@media(max-width:850px){{.layout{{grid-template-columns:1fr}}.stats{{grid-template-columns:repeat(2,1fr)}}main{{padding:14px}}}}
</style></head><body><main>
<h1>クラスタ分布マップ</h1><p class="sub">点はクラスタ、面積は所属件数、位置は768次元重心のPCA投影、線は最近傍クラスタ（cos類似度0.72以上）です。詳細には代表的な構成要素を最大5件表示します。</p>
<section class="stats" id="stats"></section>
<div class="layout"><section class="panel"><h2>意味空間の分布と関係</h2>
<div class="controls"><label><input id="edges" type="checkbox" checked> 関係線</label><label><input id="labels" type="checkbox"> 大規模クラスタ名</label><label>MOC <select id="moc-filter"><option value="">すべて</option></select></label></div>
<svg id="map" viewBox="0 0 1000 680" role="img" aria-label="クラスタの二次元分布"></svg><div class="detail" id="detail">点を選ぶとクラスタの詳細を表示します。</div>
</section><section class="panel"><h2>クラスタサイズのばらつき</h2><svg id="hist" viewBox="0 0 420 360" role="img" aria-label="クラスタサイズ別の件数"></svg>
<div class="legend"><span><i class="dot" style="background:var(--blue)"></i>MOC所属（色別）</span><span><i class="dot" style="background:var(--orange)"></i>Markdown未昇格</span></div></section></div>
<script id="data" type="application/json">{payload}</script><script>
const data=JSON.parse(document.getElementById('data').textContent),NS='http://www.w3.org/2000/svg';
const el=(n,a={{}})=>{{const x=document.createElementNS(NS,n);Object.entries(a).forEach(([k,v])=>x.setAttribute(k,v));return x}};
const fmt=new Intl.NumberFormat('ja-JP'),s=data.summary;
document.getElementById('stats').innerHTML=[['クラスタ',fmt.format(s.clusters)],['要素',fmt.format(s.members)],['中央値',s.median_size+'件'],['単独クラスタ',fmt.format(s.singletons)],['Wiki接続',fmt.format(s.linked)]].map(([l,v])=>`<div class="stat"><b>${{v}}</b><span>${{l}}</span></div>`).join('');
const map=document.getElementById('map'),pad=35,cl=data.clusters,xv=cl.map(d=>d.x),yv=cl.map(d=>d.y),extent=a=>[Math.min(...a),Math.max(...a)],xe=extent(xv),ye=extent(yv);
const scale=(v,e,min,max)=>e[1]===e[0]?(min+max)/2:min+(v-e[0])/(e[1]-e[0])*(max-min),pos={{}};
cl.forEach(d=>pos[d.id]=[scale(d.x,xe,pad,1000-pad),scale(d.y,ye,680-pad,pad)]);
const edges=el('g',{{id:'edge-layer'}}); data.relations.forEach(r=>{{const a=pos[r.source],b=pos[r.target];edges.append(el('line',{{x1:a[0],y1:a[1],x2:b[0],y2:b[1],class:'edge',opacity:Math.max(.15,(r.similarity-.72)*2)}}))}});map.append(edges);
const nodes=el('g'),colors=['var(--viz-series-1,var(--blue))','var(--viz-series-2,var(--green))','var(--viz-series-3,var(--orange))','var(--viz-series-4,var(--blue))','var(--viz-series-5,var(--green))','var(--viz-series-6,var(--orange))']; const top=new Set([...cl].sort((a,b)=>b.size-a.size).slice(0,15).map(d=>d.id));
cl.forEach(d=>{{const [x,y]=pos[d.id],r=3+Math.sqrt(d.size)*1.1,color=d.moc_id?colors[(d.moc_id-1)%colors.length]:'var(--orange)';const c=el('circle',{{cx:x,cy:y,r,class:'cluster',fill:color,opacity:.78,tabindex:0,'data-moc':d.moc_id||''}});c.setAttribute('aria-label',`クラスタ${{d.id}} ${{d.title}} ${{d.size}}件`);const show=()=>{{const examples=d.members.length?'｜構成例: '+d.members.join(' / '):'',chain=d.moc_title?'｜MOC: '+d.moc_title:'｜MOC未所属';document.getElementById('detail').textContent=`#${{d.id}}｜${{d.title}}｜${{d.size}}件｜内部類似度 ${{d.size>1?d.similarity.toFixed(3):'—'}}｜${{d.page_path?'Markdown: '+d.page_path:'Markdown未昇格'}}${{chain}}${{examples}}`}};c.addEventListener('click',show);c.addEventListener('focus',show);nodes.append(c);if(top.has(d.id)){{const t=el('text',{{x:x+r+3,y:y+4,class:'bar-label label',display:'none'}});t.textContent=d.title.slice(0,22);nodes.append(t)}}}});map.append(nodes);
document.getElementById('edges').onchange=e=>edges.style.display=e.target.checked?'':'none';document.getElementById('labels').onchange=e=>document.querySelectorAll('.label').forEach(x=>x.setAttribute('display',e.target.checked?'':'none'));
const mocFilter=document.getElementById('moc-filter'),mocs=[...new Map(cl.filter(d=>d.moc_id).map(d=>[d.moc_id,d.moc_title])).entries()].sort((a,b)=>a[0]-b[0]);mocs.forEach(([id,title])=>{{const o=document.createElement('option');o.value=id;o.textContent=title;mocFilter.append(o)}});mocFilter.onchange=e=>document.querySelectorAll('circle.cluster').forEach(c=>c.setAttribute('opacity',!e.target.value||c.dataset.moc===e.target.value?'.78':'.08'));
const hist=document.getElementById('hist'),max=Math.max(...data.histogram.map(d=>d.count));hist.append(el('line',{{x1:45,y1:320,x2:405,y2:320,class:'axis'}}));
data.histogram.forEach((d,i)=>{{const w=34,g=44,x=55+i*g,h=d.count/max*270,y=320-h;hist.append(el('rect',{{x,y,width:w,height:h,rx:3,class:'bar'}}));const n=el('text',{{x:x+w/2,y:y-7,'text-anchor':'middle',class:'bar-label'}});n.textContent=d.count;hist.append(n);const l=el('text',{{x:x+w/2,y:340,'text-anchor':'middle',class:'bar-label'}});l.textContent=d.label;hist.append(l)}});
</script></main></body></html>"""


def generate(database: Path, output: Path) -> dict[str, int]:
    clusters = load_clusters(database)
    principal_projection(clusters)
    relations = nearest_relations(clusters)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(clusters, relations), encoding="utf-8", newline="\n")
    return {"clusters": len(clusters), "members": sum(cluster["size"] for cluster in clusters), "relations": len(relations)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path("live-vault/.agent-state.sqlite3"))
    parser.add_argument("--output", type=Path, default=Path("live-vault/cluster-map.html"))
    args = parser.parse_args()
    result = generate(args.database, args.output)
    print(f"generated {args.output}: {result['clusters']} clusters, {result['members']} members, {result['relations']} relations")


if __name__ == "__main__":
    main()
