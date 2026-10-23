---
title: tester-army/e2e：用大白话写端到端测试（知识点笔记）
date: 2026-10-23
source_video: video
tags: []
---

# tester-army/e2e：用大白话写端到端测试（知识点笔记）

> 来源：微信视频号《9100 多星！用大白话写端到端测试：tester-army e2e》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
`tester-army/e2e`（GitHub ~9,153★ / Fork 441，Apache-2.0，TypeScript 98%，上线不到三个月冲上趋势榜）是**下一代 Web/移动端 AI 端到端测试框架**：测试步骤用自然语言写、AI 代理带视觉按语义操作、确定性断言 + 自由发挥混合、真实环境执行、验证过步骤缓存重放省模型额度。

## 核心要点
- **定位**：下一代 Web/移动端 AI 端到端测试框架，由 TesterArmy 团队开源维护。
- **自然语言步骤（不写选择器/不写 sleep）**：
  ```ts
  test('a member upgrades to Pro', async ({ app, agent, screen }) => {
    await app.open('/settings/billing');
    await agent.act('upgrade the workspace to the Pro plan');   // 大白话
    await agent.assert('the invoice preview shows a prorated amount');
    await expect(screen.getByRole('status')).toContainText('Pro'); // 确定性断言
  });
  ```
- **视觉定位（替代选择器）**：执行的是一个带视觉能力的 AI 代理，截图理解整个页面、像真人一样点按钮填表单、按语义定位；按钮改名/页面改版它重新看一眼即可，脚本不用改。
- **混合断言**：模糊路径/多步操作交给代理自由发挥；关键结果用确定性断言逐字核对（"执行可灵活，验收必须严格"）。
- **真实环境执行**：Web 用 Playwright 引擎（Chromium/Firefox/WebKit），Mobile 用真模拟器（iOS/Android），点真按钮、填真表单。
- **缓存重放（省额度）**：第一次运行 AI 探索并记录动作；之后验证过的步骤直接重放，**0 次模型调用**；只有应用本身改了才重新探索。
- **成品演示**：`npx e2e test tests/checkout.e2e.ts` → 跑完自动出报告（`1 passed · cache: 1 step replayed · 0 model calls`）。

## 展开说明
- **对比传统 UI 自动化**（见 `005`）：不用维护一堆选择器和等待时间，"改版一次修一遍脚本的日子到此为止"。
- 与 `033`（AITS 测试全流程）、`004/006`（软件测试提效/面试）同属测试工程主题。

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 全程 | 9,153 星/趋势榜、自然语言测试代码示例、视觉定位/混合断言/真实环境/缓存重放四特性、控制台演示与报告 |
