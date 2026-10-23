---
title: 抄 29 万人收藏的 Agent Skills 技能包（mattpocock/skills）知识点笔记
date: 2026-10-23
source_video: video
source_frames: D:/Project/wechat-knowledge/output_videos/014_Agent_Skills_怎么用？抄_29_万人收藏的大牛技能包_29_万人收藏/frames
timestamps: [00:00, 00:01, 00:03, 00:05, 00:07, 00:09, 00:11, 00:13, 00:14, 00:16, 00:18, 00:20, 00:22, 00:24, 00:26, 00:28, 00:29, 00:31, 00:33, 00:35, 00:37, 00:39, 00:41, 00:42, 00:44, 00:46, 00:48, 00:50, 00:52, 00:55]
tags: []
---

# 抄 29 万人收藏的 Agent Skills 技能包（mattpocock/skills）知识点笔记

> 来源：微信视频号《Agent Skills 怎么用？抄 29 万人收藏的大牛技能包》（李自在 AI 风向标 S1E02）
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
29 万人收藏的"大牛技能包"，其实是 **Matt Pocock 一个人的 `.agents` 目录**开源出来（[mattpocock/skills](https://github.com/mattpocock/skills)，GitHub ~29 万星 / 2.4 万 fork，MIT），给"真正工程师"用的技能集合，分**效率类**和**工程类**。

## 核心要点
**效率类（由你手动调用）**
- `grill-me`：让 AI 围绕你的计划/设计不停追问，直到决策树的每个分支都定下来（逼你想清楚）。
- `handoff`：把当前对话压缩成一份交接文档，方便另一个 Agent 接着干。
- `teach`：分几次对话教你一个新技能/概念，用当前目录记录学习进度。
- `wait-what`：看不懂 AI 回复时用它，AI 会补上你缺的背景、用大白话重讲一遍。
- 底层能力 `grilling`：grill-me / grill-with-docs / triage 等都靠它（追问引擎）。

**工程类（作者每天写代码在用）**
- `tdd`：测试驱动开发，按「红—绿—重构」循环，一次做一小块。
- `diagnosing-bugs`：排查难缠 bug 和性能退化的固定流程：先复现 → 缩小范围 → 提假设 → 加日志 → 修复 → 补回归测试。
- `code-review`：从两个方向审查改动——是否符合仓库代码规范 + 是否真的实现了需求。

## 展开说明
- **反差点**：所谓"神级技能包"不是神秘黑箱，而是作者自己每天都在用的 `.agents` 目录，主打"给真正工程师用"。
- **可直接抄**：MIT 协议、README 有非官方中文译文，照着把技能放进自己的 Agent 即可。
- 与 `022`（Claude Code 九大技能）、`028`（GitHub 9 个 Skill）、`009/010`（WorkBuddy 4 个 skill）互为"技能选型"参考。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 00:00~ | 引出"29 万人收藏竟是一个人的文件夹" + 技能清单（效率类/工程类） |
| 中段 | 仓库信息：mattpocock/skills，29 万星/2.4 万 fork/MIT，取自作者 .agents 目录 |
