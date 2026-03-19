# 企业信息 MVP

这是一个用于聚合日本企业信息的最小可用 FastAPI 后端项目。

## 语言版本

- English: [README.md](README.md)
- 中文: `README.zh-CN.md`
- 日本語: [README.ja.md](README.ja.md)

## 功能

- 支持企业搜索，并返回可区分重名公司的字段
- 支持通过 `corporate_id` 查询企业详情
- 使用 SQLite 存储企业数据和信号数据
- 支持刷新基于官网内容提取的招聘与技术信号

## 技术栈

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest

## 目录结构

```text
app/
  api/         HTTP 接口
  core/        配置与数据库初始化
  crawlers/    官网信号爬取逻辑
  models/      SQLAlchemy 数据模型
  schemas/     返回结构定义
  services/    业务逻辑
  utils/       工具函数
data/          示例数据与本地 SQLite 数据库
scripts/       初始化与刷新脚本
tests/         测试代码
```

## 启动方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed_sample_data.py
uvicorn app.main:app --reload
```

## 接口列表

- `GET /health`
- `GET /search?q=ABC`
- `GET /company/{corporate_id}`
- `POST /company/{corporate_id}/refresh-signals`

## 说明

- 这个 MVP 里，`corporate_id` 是唯一企业标识。
- 搜索结果会返回足够的信息，用来区分同名公司。
- 当前的信号刷新为同步执行。
