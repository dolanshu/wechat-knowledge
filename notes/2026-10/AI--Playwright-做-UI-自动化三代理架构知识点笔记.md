---
title: AI + Playwright 做 UI 自动化：三代理架构（知识点笔记）
date: 2026-10-23
source_video: video
tags: []
---

# AI + Playwright 做 UI 自动化：三代理架构（知识点笔记）

> 来源：微信视频号《软件测试 / 测试开发 / UI 自动化测试 / AI 提效》（AI 测试项目实战）
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
一个 AI 测试项目实战演示：用 **AI + Playwright** 做 UI 自动化，主流技术方案是**三代理架构（Planner / Generator / Healer）**——规划器拆解、生成器写脚本、修复器自愈，配套完整 E2E 框架（集成 Page Object Model）。

## 核心要点
- **课程场景**：AI 测试项目实战（AI+playwright）；环境用 Docker Desktop + MySQL 8.0 镜像 + SpringBoot 应用 + playwright-e2e。
- **主流技术方案一：三代理架构**
  - **Planner（规划器）**：拆解测试任务。
  - **Generator（生成器）**：生成测试脚本。
  - **Healer（修复器）**：失败自愈/修复。
- **框架形态**：完整 E2E 测试框架，集成 **Page Object Model**；目录含 `scripts / pageobjects / fixtures / specs / skills/ai-playwright / SKILL.md`。
- **相关 Skill/工具**：`WebappTesting`、`browser-automation-framework`、`playwright-cli`、`qodex-ai`、`skilforge-claude-plugin`、`playwright-best-practices`、`e2e-outside-in-test`。
- **运行**：`node scripts/run-tests.js`（在 AI+playwright 目录下）。

## 展开说明
- **与生态关联**：三代理（Planner/Generator/Healer）是"AI 写测试"的典型编排范式；与 `005`（UI 自动化 4 层心法）、`013`（tester-army e2e 自然语言测试）、`022`（WebappTesting 技能）互为补充。
- **价值**：把"AI 生成测试"从一次性脚本升级成"生成→自愈"的闭环。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | 课程实战环境（Docker/MySQL/SpringBoot）、三代理架构图（Planner/Generator/Healer）、E2E 框架目录与运行命令 |
