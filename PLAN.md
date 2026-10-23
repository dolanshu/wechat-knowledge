# 项目计划：微信视频 → 知识点 Markdown

> 更新：2026-10-23。P0 真数据(59 视频)已导入并全量抽帧+OCR；P3 笔记生成已大规模推进(50 篇归档)；已沉淀 wechat-video-note skill；git 已配好并推送到 GitHub。

## 现状盘点

| 组件 | 状态 |
|---|---|
| `process_video.py` | ✅ 抽帧 + MSE 去重 + 均匀抽样（`--max-frames`）+ 时间戳；支持中文/emoji 路径 |
| `ocr_frames.py` | ✅ 关键帧 → 中文 OCR（`rapidocr-onnxruntime`，模型随包自带）→ `ocr.md` |
| `archive_note.py` | ✅ 归档到 `notes/YYYY-MM/` + 重建 `notes/INDEX.md` |
| 真实视频 (P0) | ✅ 用户已导入 59 个视频/图片/音频到 `./video/` |
| 抽帧 + OCR | ✅ 59 个视频全部完成：`output_videos/` 下每目录含 `frames/` + `raw_extract.md` + `ocr.md` |
| 笔记生成 (P3) | ✅ 50 篇已归档（notes/2026-10/）；剩余 9 篇用户未勾选（见"规模与策略"） |
| 关键帧时间戳 (P1) | ✅ 帧文件名 `frame_0001_t00m12s.jpg`，`raw_extract.md`/`ocr.md` 均带时间戳 |
| 端到端验证 (P2) | ✅ Python 3.12 + `.venv`（opencv/pillow/numpy/faster-whisper/rapidocr） |
| `gen_test_video.py` | ✅ `sample/test_video.mp4` 已生成 |
| `sample/最终知识点示例.md` | ✅ 目标输出格式样例 |

## 读图能力说明（重要）

当前运行环境的多模态读图能力不可用（无法查看图片）。原计划"读关键帧"改为：
**关键帧 → 本地 OCR → `ocr.md` 文字 → 据此整理笔记**。OCR 对中文讲解句识别良好，
代码/英文画面噪声较大，整理时按需取舍。若环境日后支持读图，可跳过 OCR 直接看图。

## 规模与策略（P3 续）

59 个视频已全部抽帧 + OCR。**50 篇笔记已生成并归档**到 `notes/2026-10/`（含首轮 4 篇 + 测试示例 + 本轮用户勾选的 45 篇）。

- 已归档（50 篇）：覆盖 AI 编程/编码工具、软件测试/AI 测试、Agent/大模型/求职、运维/监控/SRE/安全、数据库/CS 基础等主题。
- 待整理（9 篇，用户未勾选）：`023/024/025`（同一 C 语言视频三份，任选其一）、`026`（DevOps）、`011`（职场吐槽）、`044`（非技术）、`021`（与 `020` 重复，跳过）。
- 后续新增视频：走 README「后续更新指南」标准动作，或由 `wechat-video-note` skill 触发。

## 执行记录（2026-10-23）

- 安装 Python 3.12 + 建 `.venv`，装 opencv/pillow/numpy/faster-whisper/rapidocr-onnxruntime。
- 修复 Windows 非 ASCII 路径（临时拷 ASCII 副本 + imencode 写文件）、GBK 控制台、长文件名截断、长视频爆量（`--max-frames`）。
- P0 真数据：59 个视频抽帧（1329 张关键帧），全量 OCR 产出 `ocr.md`。
- P3 示范 4 篇笔记并归档，打通"抽帧→OCR→整理→归档→索引"真实闭环。
- 更新 README（OCR 步骤、真实目录 `video/`、`output_videos/`、批量归档命令）与 PLAN。

## 执行记录（2026-10-23 续）

- 用户勾选 45 篇笔记全部生成并归档（`notes/` 共 50 篇）；`pending_notes.md` 标记完成。
- 配置 Git：生成 ed25519 SSH key、关联 `git@github.com:dolanshu/wechat-knowledge.git`、统一 `main` 分支、提交邮箱改为 GitHub noreply；全部已 commit + push。
- 沉淀 CodeBuddy skill：`.codebuddy/skills/wechat-video-note/SKILL.md`，固化"生成笔记 + 归档 + 入库"流程与格式规范。
- 重写 README：补进度状态、笔记格式规范、去重读取技巧、git 入库与端到端后续更新指南。

## P0 视频获取方案（新增，前置依赖）

**需求**：把某账号（视频号作者主页）的视频批量下载到 `./videos/`。

视频号无官方下载 API，所有方案本质都是本地代理拦截 / 注入脚本。按场景选型：

| 场景 | 推荐方案 | 说明 |
|---|---|---|
| 单个视频（转发给自己的收藏） | 网页解析 / 小程序机器人 | 现有 README 方案，零安装 |
| **某账号主页批量** | `ltaoo/wx_channels_download`（GitHub，持续更新）或 Gitee `rodert/WeixinVideoDownload` | 后者明确支持"主页批量下载、按作者自动分类"；原理均为注入下载按钮/采集主页视频列表 |
| 顺手抓多个平台 | `res-downloader`（开源） | 本地代理嗅探，支持视频号/抖音/小红书等 |

**批量下载通用流程**：安装工具并信任其本地根证书（一次性）→ 微信内打开该作者主页 → 工具拦截主页信息流接口并列出全部视频 → 批量下载到本地 → 拷入 `./videos/`。

**风险**：
- 第三方工具随微信版本更新可能失效，需选活跃维护的项目（`wx_channels_download` 2025-10 仍在发版）。
- 仅限个人学习用途，勿二次传播（版权）。
- 网页解析/小程序机器人方案内容经过第三方服务器，隐私敏感内容避免使用。

## P1 关键帧时间戳（小改动，先做）

- 抽帧时记录 `帧序号 → 视频时间`（`time = 解码帧号 / video_fps`）。
- 落盘两处：帧文件名改为 `frame_0001_t00m12s.jpg`；`raw_extract.md` 帧清单追加时间列。
- 效果：最终知识点笔记可带时间戳，回看视频可定位。
- **可行性：高**。改动集中在 `extract_key_frames()` 约 20 行，无新依赖。

## P2 端到端验证（跑通全链路）

1. 安装 Python 3.12+（本机当前无 Python；沙箱允许联网，可用 winget/uv 安装，或由用户在自己机器执行）。
2. `pip install -r requirements.txt`。
3. `python gen_test_video.py` 生成 `sample/test_video.mp4`。
4. `python process_video.py -i ./sample/test_video.mp4 --no-transcribe`。
5. 验证 `output/test_video/frames/` 关键帧数量合理（预期 ~5 张，对应 5 屏）、`raw_extract.md` 内容正确。
6. 我读关键帧产出知识点 Markdown，与 `sample/最终知识点示例.md` 格式对齐。
- **可行性：高**。opencv-python-headless 有 3.12/3.13 轮子；主要成本是环境搭建。风险：无。

## P3 提取 → 笔记自动衔接

- 基线（零开发）：提取完成后直接在对话里让我读 `output/<视频名>/` 出笔记——现在就能做，写成 README 的标准操作步骤。
- 进阶（可选）：封装 CLI/skill 调多模态 API 批量生成笔记，需要 API Key，仅当批量量大再做。
- **可行性：基线 100%；进阶中**（依赖 API Key 与费用考量）。

## P4 知识库归档

- 目录约定：`notes/YYYY-MM/<标题>.md`，front-matter 含来源视频、日期、时间戳链接。
- 生成 `notes/INDEX.md` 索引（标题 + 一句话总结 + 来源）。
- **可行性：高**。纯文件约定 + 小脚本。

## 里程碑顺序

```
P0 选定下载工具并导入首批视频  ──┐
P1 时间戳支持（可与 P0 并行）   ──┼─→ P2 端到端验证 ─→ P3 衔接 ─→ P4 归档
```

P1、P2 不依赖 P0，可立即开工；P3/P4 在 P2 验证通过后推进。
