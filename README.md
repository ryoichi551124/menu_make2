# 献立提案AIアプリ

### ユーザーが選んだ主菜から、それに合う副菜と汁物を提案するAIアプリです。

ユーザー登録なしでもご利用頂けます。

ユーザー登録をすると、ユーザーが選んだ組み合わせを学習、提案します。

## http://35.193.231.227/menu/

![スクリーンショット 2021-03-23 10 14 13](https://user-images.githubusercontent.com/60164700/112081723-786b9000-8bc7-11eb-80a8-d80adad86b3f.png)

![スクリーンショット 2021-03-23 10 17 22](https://user-images.githubusercontent.com/60164700/112081784-989b4f00-8bc7-11eb-9482-5312e30abcc1.png)



## 機能一覧
- ユーザー登録、ログイン機能、ゲストログイン
- LightGBMを使用したAIモデルの実装
- 登録ユーザーごとの学習機能

## 技術一覧
### WEBアプリ
- Anaconda仮想環境
- python 3.8.2
- django 3.0.4
- SQLight(django default)
- GCP
  - GCE
    - os Ubuntu 18.0.4LTS
    - Nginx
    - gunicorn
  - VPCネットワーク

### データ取得
- rakuten recipe API

      https://webservice.rakuten.co.jp/api/recipecategorylist/

      https://webservice.rakuten.co.jp/api/recipecategoryranking/

      データ取得コード(google colaboratory)

      https://colab.research.google.com/drive/1J3xK23hYKfyY8g-DzAH5AFifyLNlFV41?usp=sharing

### AIモデル作成
- LightGBM
- MeCab(形態素解析）
- google colaboratory
   - データ前処理①　　　　https://colab.research.google.com/drive/1afCGmKPDGi8tcES_xkSGVurUvRucNBFS?usp=sharing　
   - データ前処理②　　　　https://colab.research.google.com/drive/1LqiluQ59SRFTZbz9A9d5JwGeXctakLSm?usp=sharing
   - データ前処理③　　　　https://colab.research.google.com/drive/1-sFifkQd1nN9UVxJV2uXQc3XUQofCDFx?usp=sharing
   - データ前処理④　　　　https://colab.research.google.com/drive/19QTDg5GvlKD5GPC_5xV32FcQQtUf5s56?usp=sharing
   - モデル作成①　　　　https://colab.research.google.com/drive/1fulISoXtKXcRWKEigNhdsxpkoSLpAVyc?usp=sharing
   - モデル作成②　　　　https://colab.research.google.com/drive/1YRGeQSSZOY3ueVdQNWvm0WMdAoPgfRMI?usp=sharing
   - モデル作成③　　　　https://colab.research.google.com/drive/19xqJyd5j5VM8hfDkWwEw9QYZrFdKA-Ui?usp=sharing



## 献立提案AIアプリ　デプロイ手順

---

## linuxサーバーにSSH接続
- anacondaインストーラーの取得
`wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh`

- パッケージのアップデート
`sudo apt update`

- anacondaのインストール
`bash Anaconda3-2022.10-Linux~ (途中でタブ補完) `
(yes ２回（2回目はデフォルトで no になっているので注意)

- bashファイルにanacondaのパスの設定
`source ~/.bashrc`

- 仮想環境の作成
`conda create -n 仮想環境名 python=3.9.?`
(当時はインストーラーpython3.7.2)

- 仮想環境に入る
`conda activate 仮想環境名`
`which python` で python の確認

- anacondaインストーラーの削除
`rm Anaconda3-2022.10-Linux~ (途中でタブ補完)`

- Githubからクローンする
`git clone https://github.com~`
cdコマンドでアプリフォルダへ移動

- パッケージのインストール
`pip install -r requirements.txt`
- 確認
`pip list`

- nginxのインストール
`sudo apt-get install nginx`

- nginx の動作確認
`ps aux | grep nginx`

- gunicorn の確認
`which gunicorn`

- gunicorn の手動接続
`gunicorn アプリフォルダ名.wsgi —bind=0.0.0.0:8000`

- gunicorn の自動化設定
`sudo vi /etc/systemd/system/gunicorn.service`
- ユーザー名の確認
`echo $USER`

gunicorn.serviceのファイル記述
```
[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=ユーザー名
Group=ユーザー名
WorkingDirectory=/home/ユーザー名/menu_make
ExecStart=/home/ユーザー名/anaconda3/envs/menu_make/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/puducerk/menu_make/menu_make.sock menu_make.wsgi:application
[Install]
WantedBy=multi-user.target
```


-- gunicorn を動作させる
`sudo systemctl start gunicorn`

- gunicorn の動作確認
`ps aux | grep gunicorn`

- シンボリックリンクの設定
`sudo systemctl enable gunicorn`

- nginx の設定
`sudo vi /etc/nginx/sites-available/conf`

confファイルの記述
```
server {
        server_name IPアドレス;
        location / {
                include proxy_params;
                proxy_pass http://unix:/home/ユーザー名/menu_make/menu_make.sock;
                }
        location /static {
                root /home/ユーザー名/menu_make;
        }
}
```

- シンボリックリンクの設定
`sudo ln -s  /etc/nginx/sites-available/conf /etc/nginx/sites-enabled/`

-  nginx の再起動
`sudo systemctl restart nginx`

- 各種サーバーの動作確認
`ps aux | grep nginx`
`ps aux | grep gunicorn`

<web での動作確認>
`http://IPアドレス/menu`
