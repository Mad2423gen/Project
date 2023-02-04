# Scray_cloudworks-2023-02-04
クラウドソーシングサービス、『クラウドワークス』の新規案件情報を取得してPushbulletというアプリに通知するツールです

【準備】
・Pushbulletトークンの取得・モジュールの使用方法
    ここを参考にしてください　https://laboratory.kazuuu.net/install-and-use-the-pushbullet-library-in-python/
・クラウドワークスで、必要とする案件を検索し、新着一覧で並べ直したあと、そのURLをコピーし、'clwdworks_url'ファイルに一行ずつ貼り付けておく
・’pushbullet_token’ファイルを作成して取得したトークンを１行目に貼り付ける

【開発環境】
  ・"Linux Mint" VERSION="21.1 (Vera)"　with Pycharm 2022.3.2
  ・Python3.10　外部モジュールは requrements.txt参照
 
 【使い方】
 仮想環境（venv)にて requrements.txtから外部モジュールをインストール
 ターミナルでカレントディレクトリを移動後、ディレクトリに移動後、python3 clowdworks_scray.pyを実行
 メニュー表示で１か２を選択、初めて実行するときは２を選択して情報を保存してください。
 インターバルタイムを指定すると定期的にその間隔で実行します。
 新規情報があればPushbulletへ送信されます。
 
 
