---
title: VMware Appliance OVF プロパティの CLI による更新方法
type: knowledge
status: draft
created: 2026-10-23
updated: 2026-10-23
confidence: medium
---

# VMware Appliance OVF プロパティの CLI による更新方法

## 結論

VMware Appliance OVF Properties を CLI で更新する方法は、vCenter にアクセスできない状況において、VM に直接 root 権限でログインし、`ovfenv` コマンドを使用して現在のプロパティを確認し、特定のスクリプトを実行することで設定を変更する手法であり、VM の再起動が必要な手順として明確に記載されている。このプロセスは、OVF プロパティが VM のローカルファイルシステムに保存されているため、直接編集可能な点が特徴であり、運用上の柔軟性を高める重要な手段である。

## テーマ概要

VMware Appliance OVF Properties update through CLI は、VMware アプライアンスの OVF プロパティをコマンドラインインターフェース（CLI）を通じて更新する方法についての話題です。このテーマは、vCenter（VC）へのアクセスができない状況でも、ESX UI から VM に直接アクセスして OVF プロパティを変更する必要がある場合に特に注目されています。OVF プロパティは、VM の設定情報（例：ホスト名、IP アドレス、NTP サーバーなど）を含むため、これらの設定を変更する必要があるケースがよくあります。特に、ネットワーク設定やタイムゾーン設定など、運用上の柔軟性を求める場面で、CLI を通じた更新方法が求められます。また、この方法は、vCenter に依存せず、直接 VM にアクセスできる環境での運用に適しており、クラウドや仮想化環境における柔軟な管理手法として注目されています。

## 共通して確認できる点

VMware Appliance OVF Properties を CLI で更新する方法について、複数の記事で共通して確認できた事実があります。この方法は、vCenter にアクセスできない場合に特に有用です。VM に root 権限でログインし、`ovfenv` コマンドを使用して現在の OVF プロパティを確認します。OVF プロパティは、VM のローカルファイルシステムに保存された構成ファイルで、直接編集可能です。例えば、NTP サーバーの設定を変更するには、`/opt/vmware/vcf/commonsvcs/scripts/ntp/` ディレクトリ内の `update-ntp_server.sh` スクリプトを新しい NTP サーバーの IP アドレスを指定して実行します。変更後は、VM を再起動する必要があります。また、OVF プロパティの変更には、特定のスクリプトやディレクトリが関与しており、それらは特定の目的で設計されています。このプロセスは、root 権限が必要であり、変更を反映させるためには再起動が必須です。

## 記事ごとの差分・視点の違い

記事「VMware Appliance OVF Properties update through CLI」は、vCenterにアクセスできない場合でも、ESX UI経由でVMに直接アクセスしてOVFプロパティをCLIで更新する方法を説明しています。このアプローチは、VMのローカルファイルシステム内の設定ファイルを編集することで、NTPサーバーなどの設定を変更する例が挙げられています。この記事は、VMware ApplianceのOVFプロパティを直接変更するための実践的な手順を提供しています。

記事「Run VMware OVF Tool From the Command Line」は、OVF Toolの基本的な使い方を説明しており、OVFパッケージを検証・展開するためのコマンドライン操作に焦点を当てています。この記事は、OVF Toolの使用方法を解説しており、OVFプロパティの変更ではなく、OVFパッケージの操作に特化しています。

記事「How I Did the Multi-VM Monitoring」は、複数の仮想マシンを監視する際の課題を紹介しており、メトリクスのタグ付けに失敗した経験をもとに、設定値がコードに正しく伝達されるかを確認する必要性を強調しています。この記事は、監視システムの設計における実際の課題とその解決策を示しています。

記事「How I Did the Multi-VM Monitoring – Sciencx」は、前記の記事と同様のテーマを扱っており、設定値がコードに伝達されない問題についてさらに掘り下げています。この記事は、設定値が設定ファイルに存在しているにもかかわらず、実行中のプログラムに届かないという問題点を指摘し、設定の確認が重要であることを示しています。

記事「vmwmouse/README.md at main · NattyNarwhal/vmwmouse · GitHub」は、Windows 3.1用のマウスドライバーについて説明しており、VMwareやQEMUでの使用を可能にします。このドライバーは、PS/2マウスドライバーの代替として動作し、絶対位置の座標を送信してカーソルの制御を可能にします。この記事は、仮想環境でのマウス操作の改善に貢献する可能性のあるドライバーの紹介をしています。

## 深掘り調査で得られた知見

VMware Appliance OVF Properties を CLI で更新する方法について、深掘り調査によりいくつかの知見が得られました。この方法は、vCenter へのアクセスができない場合に特に有用です。VM に root 権限でログインし、`ovfenv` コマンドを使用して現在の OVF プロパティを確認します。OVF プロパティは、VM のローカルファイルシステムに保存されており、直接編集可能です。例えば、NTP サーバーの設定を変更するには、`/opt/vmware/vcf/commonsvcs/scripts/ntp/` ディレクトリ内の `update-ntp_server.sh` スクリプトを新しい NTP サーバー IP アドレスで実行します。変更後は、VM を再起動することで新しい設定が反映されます。このプロセスは、特定のスクリプトやディレクトリを使用して行われ、root 権限が必要です。また、OVF プロパティの変更には、VM の再起動が必須です。この方法は、vCenter へのアクセスができない場合に現実的な解決策として位置付けられています。一方、他のドキュメントでは、OVF Tool の使用や vSphere API および PowerCLI の利用が紹介されていますが、これらは OVF プロパティの変更ではなく、OVF パッケージのデプロイや確認に焦点を当てています。したがって、CLI を通じた OVF プロパティの直接編集は、特定のシナリオにおいて非常に有効なアプローチです。

## 不確実な点・追加確認が必要な点

記事間で確認できた情報には、VMware Appliance の OVF Properties を CLI で更新する方法に関する記述が含まれています。しかし、各記事の内容にはいくつかの違いや不明点があります。例えば、記事 1 では、OVF Properties を更新する際には、VM に root アクセスが必要であり、特定のスクリプト（例: `update-ntp_server.sh`）を実行することで設定を変更する方法が説明されています。一方で、記事 2 では、OVF Tool を使用して OVF パッケージを検証・展開する方法が説明されており、OVF Properties 自体を直接編集する手順には触れていないため、記事 1 と記事 2 は別の目的を持つ技術的アプローチとして分離されています。

また、記事 1 では、OVF Properties が VM のローカルな構成ファイルに保存されていると述べられており、このファイルを直接編集することで設定を変更できるとされています。しかし、具体的なファイル名や場所は記述されておらず、読者には自己責任で探索する必要がある点が挙げられます。一方、記事 2 では、OVF Tool の使用方法が説明されており、これは OVF パッケージの検証や展開に特化したツールであり、OVF Properties の編集には関係がありません。

さらに、記事 1 では、変更後の設定を有効化するには VM の再起動が必要であると述べられており、これは設定変更の副作用として重要です。しかし、記事 2 では、OVF Tool の使用方法が説明されているため、OVF Properties の変更とは直接関係がありません。このように、記事 1 は OVF Properties の CLI での変更に焦点を当てている一方で、記事 2 は OVF Tool の使用方法を説明しており、両者は異なる目的を持つ技術的アプローチとして扱われています。

また、記事 1 では、OVF Properties を変更する際には、`ovfenv` コマンドを使用して現在の設定を確認する必要があるとされています。しかし、このコマンドの具体的な使用法や出力結果については、記事内で詳細に記述されていません。そのため、読者にはこのコマンドの使用方法を自分で確認する必要がある点が挙げられます。一方で、記事 2 では、OVF Tool の使用方法が詳細に説明されており、OVF パッケージの検証や展開に関する情報が豊富に提供されていますが、OVF Properties の編集には関係がありません。

これらの違いから、記事 1 と記事 2 は、OVF Properties の CLI での変更と OVF Tool の使用という異なる目的を持つ技術的アプローチとして分離されています。そのため、OVF Properties の CLI での変更に関する情報は、記事 1 に集中しており、他の記事ではそのような情報は提供されていません。また、記事 1 では、OVF Properties の変更には root アクセスと VM の再起動が必要であると述べられており、これは設定変更の手順として重要ですが、他の記事ではこの点について触れていません。

## 元記事一覧

- [VMware Appliance OVF Properties update through CLI](https://dev.to/ashishchorge/vmware-appliance-ovf-properties-update-through-cli-1mh2)
- [Run VMware OVF Tool From the Command Line](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere-sdks-tools/8-0/ovf-tool-user-s-guide/using-ovf-tool-commands/definitions-and-command-syntax/run-vmware-ovf-tool-from-the-command-line.html)
- [HowididtheMultiVMmonitoring- DEV Community](https://dev.to/techwithhari/how-i-did-the-multi-vm-monitoring-2ef1)
- [HowididtheMultiVMmonitoring– Sciencx](https://www.scien.cx/2026/09/01/how-i-did-the-multi-vm-monitoring/)
- [vmwmouse/README.md at main · NattyNarwhal/vmwmouse · GitHub](https://github.com/NattyNarwhal/vmwmouse/blob/main/README.md)
