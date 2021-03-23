# 献立提案AIアプリ

### ユーザーが選んだ主菜から、それに合う副菜と汁物を提案するAIアプリです。
## http://35.193.231.227/menu/



## 機能一覧
- 認証機能（ゲスト or 新規登録)
- LightGBMを使用したAIモデルの実装
- 登録ユーザーごとの学習機能

### 技術一覧
WEBアプリ
- Anaconda仮想環境
- python 3.8.2
- django==3.0.4
- SQLight(django default)
- GCP
  - GCE
    - os Ubuntu 18.0.4LTS
    - Nginx
    - gunicorn
  - VPCネットワーク

データ取得
- rakuten recipe API

      https://webservice.rakuten.co.jp/api/recipecategorylist/


























