# 企業情報 MVP

日本企業情報を集約するための最小構成の FastAPI バックエンドです。

## 言語版

- English: [README.md](README.md)
- 中文: [README.zh-CN.md](README.zh-CN.md)
- 日本語: `README.ja.md`

## 主な機能

- 同名企業を見分けるための補助情報付き企業検索
- `corporate_id` による企業詳細取得
- SQLite による企業データとシグナルデータの保存
- 企業サイトから採用・技術シグナルを再取得する機能

## 技術スタック

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest

## ディレクトリ構成

```text
app/
  api/         HTTP エンドポイント
  core/        設定と DB 初期化
  crawlers/    Web サイトシグナル取得
  models/      SQLAlchemy モデル
  schemas/     レスポンススキーマ
  services/    ビジネスロジック
  utils/       ヘルパー関数
data/          サンプルデータとローカル SQLite DB
scripts/       初期投入・更新スクリプト
tests/         テスト
```

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed_sample_data.py
uvicorn app.main:app --reload
```

## API 一覧

- `GET /health`
- `GET /search?q=ABC`
- `GET /company/{corporate_id}`
- `POST /company/{corporate_id}/refresh-signals`

## 補足

- この MVP では `corporate_id` を唯一の企業識別子として扱います。
- 検索結果には同名企業を判別するための情報を含めています。
- シグナル更新は現時点では同期実行です。
