---
title: Karpathy 新思想落地：Skill answer-me-with-html（知识点笔记）
date: 2026-10-23
source_video: video
source_frames: D:/Project/wechat-knowledge/output_videos/032_Karpathy_新思想落地！开源_Skill_answer-me-with-h/frames
timestamps: [00:00, 00:01, 00:02, 00:03, 00:04, 00:05, 00:06, 00:08, 00:09, 00:10, 00:11, 00:12, 00:13, 00:14, 00:15, 00:16, 00:17, 00:18, 00:19, 00:20, 00:21, 00:22, 00:23, 00:24, 00:25]
tags: []
---

# Karpathy 新思想落地：Skill answer-me-with-html（知识点笔记）

> 来源：微信视频号《Karpathy 新思想落地！开源 Skill answer-me-with-html 来了》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
把 Karpathy"让 AI 用最少文字讲清核心信息"的想法落地成开源 Skill **`answer-me-with-html`**：让 AI Agent 用**一页 HTML** 回答复杂问题，对比直接要 HTML，**Token 省 7.4 倍、速度快 3.6 倍**。

## 核心要点
- **做法**：让 AI 输出一页 HTML（而非长段文字），用可视化/结构化页面讲清复杂问题。
- **实测对比**（视频数据）：
  - 直接 Ask for HTML：~6,873 token / ~50s
  - 用该 Skill：~893 token / ~13s → **3.6× faster**、约 **7.4× 更省 token**
- **特性**：内置 Shadcn 两套 UI 风格、支持 Blueprint、Claude Code plugin、支持中文、可生成 3Blue1Brown 风格讲解视频（explainervideos）；项目 Star 持续暴涨。

## 展开说明
- **为什么有效**：复杂问题（如 TCP 三次握手）用一页交互式 HTML 远比纯文字省 token 且更直观；把"表达成本"转成结构化渲染。
- **适用**：向 AI 要"复杂概念解释/对比/示意图"时，要求输出 HTML 而非长文。
- 与 `009/010`（WorkBuddy Skill 生态）、`022`（SkillCreator）同属"Skill 化工作流"范畴。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | Skill 介绍、Token/速度对比表、UI 风格、安装方式（Claude Code plugin）、项目 Star 暴涨 |
