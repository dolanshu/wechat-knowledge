---
title: Qodo PR-Agent：自动做"最后 1% 代码审查"（知识点笔记）
date: 2026-10-23
source_video: video
tags: []
---

# Qodo PR-Agent：自动做"最后 1% 代码审查"（知识点笔记）

> 来源：微信视频号《团队 99% 的代码，都是 AI 生成的？Qodo 开源的 PR-Agent》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
`Qodo PR-Agent` 是开源的 AI 代码审查代理（社区维护，LAST COMMIT TODAY）：当团队 **99% 代码由 AI 生产**时，它能自动完成"最后 1% 的人工审查"——与 GitHub / GitLab / Bitbucket / Azure DevOps 无缝集成，高量自动化 PR 审查。

## 核心要点
- **项目**：PR-Agent（原创开源公关评论员），开源的、基于人工智能的代码审查代理；Qodo 的一个由社区维护的遗留项目（与 Qodo 商业审查产品不同，后者功能更丰富且有上下文感知；Qodo 为开源项目提供免费版本）。
- **背景论点**：团队 99% 代码 AI 生成 → 真正稀缺的是"自动审查这最后 1%"。
- **能力**：帮你检查代码；可与 GitHub、GitLab、Bitbucket、Azure DevOps 集成，实现高量自动化审查。
- **状态**：活跃维护（LAST COMMIT TODAY），有金牌赞助商支持。

## 展开说明
- **定位互补**：与 `016`/`017`（人工 code review 方法论）、`028`（code-review 技能）、`048` 的 DESIGN.md 体系同属"AI 代码质量保障"工具链——PR-Agent 把审查自动化。
- **适用**：AI 重度产码的团队，用它在合并前自动跑一轮审查。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | PR-Agent 仓库页、开源/AI 审查代理定位、99% 代码 AI 生成论点、多平台集成 |
