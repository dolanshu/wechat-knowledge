---
title: LoopX：给长时运行 AI 智能体团队的本地控制台知识点笔记
date: 2026-10-23
source_video: video
source_frames: D:/Project/wechat-knowledge/output_videos/040_再也不用担心_AI_干长活儿干到一半失联了！_LoopX_给你的_AI_智能体团/frames
timestamps: [00:00, 00:01, 00:02, 00:05, 00:06, 00:07, 00:08, 00:09, 00:10, 00:11, 00:12, 00:13, 00:14, 00:16]
tags: []
---

# LoopX：给长时运行 AI 智能体团队的本地控制台知识点笔记

> 来源：微信视频号《再也不用担心 AI 干长活儿干到一半失联了！LoopX 给你的 AI 智能体团队装上一个本地控制台》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
`LoopX` 是给**长时运行 AI 智能体团队**的"本地控制台"（local control plane）：目标、回合、待办、证据、用量一目了然，让 AI 干几百小时的长活儿也不跑偏、不失联。

## 核心要点
- **定位**：The local control plane for long-running AI agent work —— 长任务中的"人工判断、Agent 节奏、持久状态"稳定器。
- **特性**（来自 README/视频）：
  - 支持 `Codex` / `Claude Code` / `Cursor`
  - `Python 3.11+`，标准库实现，**零外部服务**
  - 可管理 **200+ 小时**的长时任务
  - **本地优先**，不依赖云端
  - 多智能体团队，支持**所有权移交**（handoff）
- **展示面板**：Objective / Turn（如 3/5）/ Todo / Action / Done / Evidence Log / 用量，全程可追溯。

## 展开说明
- **痛点**：AI 干长活儿容易中途失联、目标漂移；LoopX 用"回合可控 + 证据留存 + 目标锁定"解决。
- **适用**：需要让 Agent 团队跑数小时/数天的研发或研究任务时，作为本地协调与监督层。
- 仓库：`github.com/loopx`。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | README/面板展示：LoopX 定位、特性清单、目标/回合/证据面板、github 地址 |
