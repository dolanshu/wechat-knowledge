---
title: PentAGI：完全自主的 AI 红队工具（知识点笔记）
date: 2026-10-23
source_video: video
tags: []
---

# PentAGI：完全自主的 AI 红队工具（知识点笔记）

> 来源：微信视频号《完全自主的 AI 红队工具 PentAGI，多个 AI 代理互相协作，自主入侵目标系统》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
`PentAGI`（Penetration testing Artificial General Intelligence）是**开源、自托管**的完全自主 AI 红队工具：用自然语言描述目标和系统，一组专门的 AI agents 自主规划、在隔离 Docker 沙箱里运行 **20+ 专业渗透工具**（nmap / Metasploit / sqlmap），记住学到的东西并交出报告，**全程零人工干预、100% 开源（MIT）**，上线即冲上 GitHub 日趋势第一。

## 核心要点
- **形态**：开源、自托管、多目标；MIT license；Repository of the Day #1。
- **工作方式**：你用自然语言描述 target + goal → 一组专门的 AI agents 互相通信协作，规划工作、运行 20+ 专业工具、记住学习结果、输出报告。
- **隔离**：工具跑在隔离的 Docker sandbox 内（nmap/Metasploit/sqlmap），降低对宿主风险。
- **热度**：在 REA 热度后跟上，抢下 GitHub 日趋势第一；社区评价"这波开源直接封神""100% 开源，不用人一步步操作"。

## 展开说明
- **定位**：自主渗透入侵工具，多 AI Agent 协同攻击目标系统，攻击过程无需人工介入。
- **合规提醒**：渗透测试工具，仅可用于**授权的**安全测试/红队演练，严禁未授权使用（涉及法律风险）。
- 与 `043`（开源 SRE Agent 框架）同属"多 Agent 自主执行专业任务"范式，但方向相反（攻击 vs 运维）。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | PentAGI 仓库页（MIT/开源/日榜第一）、自然语言目标描述、多 Agent 协作入侵、Docker 沙箱 20+ 工具、报告输出 |
