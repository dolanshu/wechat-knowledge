---
title: ECC：黑客松冠军开源的"AI 编码操作系统"（知识点笔记）
date: 2026-10-23
source_video: video
source_frames: D:/Project/wechat-knowledge/output_videos/020_Anthropic_黑客松冠军开源_ECC：61_智能体+246_技能通吃_7/frames
timestamps: [00:00, 00:01, 00:02, 00:03, 00:04, 00:05, 00:06, 00:07, 00:08, 00:09, 00:10, 00:11, 00:12, 00:13, 00:14, 00:15, 00:16, 00:17, 00:18, 00:19, 00:20, 00:21]
tags: []
---

# ECC：黑客松冠军开源的"AI 编码操作系统"（知识点笔记）

> 来源：微信视频号《Anthropic 黑客松冠军开源 ECC：61 智能体+246 技能通吃 7 大 AI 编码工具》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
纽约黑客马拉松冠军（@AnthropicAI × forumventures）开源的 **ECC**（开发者 affaan-m 耗时约 10 个月），把"AI 编码操作系统"做成一套 **harness 性能优化系统**：内置上百技能 + 数十智能体，通吃 **7 大 AI 编码工具**（Claude Code / Codex / Cursor / OpenCode / Gemini / Kiro …），MIT 协议。

## 核心要点
- **定位**：The system, not the configs —— 给 AI 编程 harness（壳/运行框架）做性能优化，口号"打造全套 AI 编码操作系统 ECC"。
- **规模**（不同周次统计口径不同）：早期 ~183 技能 + 48 智能体；后续版本（ECC 2.0）~246 技能 / 61~64 智能体、7 大 harness 通吃。
- **内置能力举例**：`harness-optimizer`、`code-reviewer` / `code-review`、`continuous-agent-loop`、`code-architect`、`feature-dev`、`code-simplifier`、`checkpoint`、`autonomous-loops`、`context-budget`、`mcp-server-patterns`、`e2e-runner`、`build-error-resolver`、`codebase-onboarding`、`database-reviewer`、`docs` / `doc-operator`、`gan-generator` / `gan-evaluator` / `gan-planner`（agent 生成/评估/规划）、`nextjs-turbopack`、`go-test` 等。
- **跨工具**：ClaudeCode / Codex / Cursor / OpenCode / Gemini / Kiro …（"7 HARNESSES ECC 2.0"）。

## 展开说明
- **同类参照**：与 `028`（ECC 20 万★ 性能优化全家桶）、`029`（同项目，25 万星/30 秒装好/64 Agent）是同一项目不同周的报道，可合并理解。
- **价值**：把"调 Agent 跑 coding"从零散 prompt 升级成可复用、跨 IDE 的 harness 编排系统。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | ECC 2.0 构成（Skills/Agents/Commands 列表）、7 大 harness、内置模块清单、MIT 开源 |
