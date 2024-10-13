# CoinGlass スクレイピングプロジェクト

このプロジェクトは、CoinGlass のウェブサイトから暗号通貨とカテゴリのデータをスクレイピングし、データを JSON 形式で Webhook に送信する Python スクリプトです。

## 必要条件

- Python 3.12
- `pip` パッケージマネージャー

## セットアップ

1. リポジトリをクローンします。

    ```sh
    git clone <リポジトリURL>
    cd <リポジトリディレクトリ>
    ```

2. 仮想環境を作成し、アクティブにします。

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Windows の場合は .venv\Scripts\activate
    ```

3. 必要なパッケージをインストールします。

    ```sh
    pip install -r requirements.txt
    ```

4. `.env` ファイルを作成し、必要な環境変数を設定します。

    ```env
    WEBHOOK_URL=<あなたのWebhook URL>
    ```

## 実行方法

以下のコマンドでスクリプトを実行します。

```sh
python main.py
