# 献立提案AIアプリ

### ユーザーが選んだ主菜から、それに合う副菜と汁物を提案するAIアプリです。

ユーザー登録なしでもご利用頂けます。

## http://35.193.231.227/menu/



## 機能一覧
- ユーザー登録、ログイン機能、ゲストログイン
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
      
      https://webservice.rakuten.co.jp/api/recipecategoryranking/
      
      データ取得コード(google colaboratory)
      
      https://colab.research.google.com/drive/1J3xK23hYKfyY8g-DzAH5AFifyLNlFV41?usp=sharing
      
AIモデル作成
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




























