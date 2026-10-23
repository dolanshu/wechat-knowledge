---
title: OpenSRE：开源 SRE Agent 框架（知识点笔记）
date: 2026-10-23
source_video: video
tags: []
---

# OpenSRE：开源 SRE Agent 框架（知识点笔记）

> 来源：微信视频号《线上出事让 AI 来修：开源 SRE Agent 框架（接你已有的 60+ 工具，自己定工作流）》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
`OpenSRE`（`github.com/Tracer-Cloud/opensre`，Apache-2.0，**11.9k 星**）是一个开源 **AI SRE / DevOps Agent 框架**：把你已经在用的 **60+ 工具**（Grafana、K8s、PagerDuty、Slack、GitHub…）接进来、自己定义工作流，在**自己的基础设施**上诊断/修复/优化生产系统——**数据不出门**。

## 核心要点
- **定位**：搭你自己的 AI SRE Agent；开源框架 Apache 2.0，60+ 工具即插即连。
- **工作方式**：把已经在用的 60+ 工具接进来 → 自己定义工作流 → 在自有基础设施上回答生产环境问题；AI DevOps agent 帮你**诊断、修复、优化**线上系统。
- **数据不出门**：跑在自己的基础设施（"数据不出门"是核心卖点，对应合规/隐私）。
- **集成广度（举例）**：
  - AI/LLM：Anthropic / OpenAI / Codex / Ollama / Gemini / OpenRouter / Bedrock / NIM
  - 可观测：Grafana(Loki/Mimir/Tempo) / Datadog / Honeycomb / CloudWatch / Sentry / ES / New Relic
  - 基础设施：AWS(S3/Lambda/EKS/EC2/Bedrock) / Azure / Yandex / K8s / ArgoCD / Helm
  - 数据库：Mongo / ClickHouse / PostgreSQL / MySQL / MariaDB / Redis / Snowflake / Supabase / RDS
  - 数据平台：Airflow / Kafka / Prefect / RabbitMQ / Dagster / Temporal
  - 研发：GitHub / GitLab / Bitbucket / Jenkins
  - 管理：PagerDuty / Opsgenie / Jira / ServiceNow / Linear
  - 沟通：Slack / Discord / Telegram / WhatsApp / Notion / Confluence

## 展开说明
- **与生态关联**：与 `051`（PentAGI，多 Agent 自主执行专业任务，方向相反·攻击）同属"多 Agent 自主执行"范式；与 `054`（监控工具 Nagios/Grafana/Prometheus/Zabbix）是它要接入的上游数据来源。
- **价值**：把"线上出事人工救火"升级成"Agent 在自有环境自主诊断修复"，且强调数据主权。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | OpenSRE 仓库页（11.9k 星）、核心定位（60+ 工具/自有基础设施/数据不出门）、集成分类清单 |
