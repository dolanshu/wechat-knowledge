# 微信视频 -> 知识点 Markdown 提取工具

把你在微信里"转发给自己"的视频号内容，自动提取成可检索的知识点 Markdown。

## 整体流程

```
视频号视频
  └─ 下载器（一键 / 网页 / 机器人） -> mp4 文件
        ├─ process_video.py 抽帧 + 去重  -> 关键帧 (画面文字/图表)   ← 你的视频主要走这
        └─ process_video.py Whisper 转写 -> 语音文字 (有旁白才用)
              ↓ 把 output/<视频名>/ 发给我
         我(多模态)读图+理解 -> 知识点 Markdown
```

设计要点：你这类视频很多"信息在画面里、没有语音"，所以**抽帧是主通道**；
抽出来的帧用帧间差异去重，只留真正变化的"关键帧"，数量可控、不淹死人；
最终的读图理解和知识点整理由我来做（我能看懂图表/上下文，比裸 OCR 更准）。

---

## 第一步：把视频号视频弄下来（唯一需要你点的步骤）

视频号默认不允许"保存"，按场景选择：

### 单个视频（转发给自己的收藏）
1. **本地客户端一键下载（最推荐，隐私最好）**
   - GitHub 项目：`ThinkerWen/wechat-downloader`（Python，mitmproxy 本地代理自动嗅探+解密）
     或搜索 "微信视频号下载器 Go" 的客户端（~7k★，装一次后在视频号里直接多一个"下载"按钮）。
   - 需要信任并安装一个**本地根证书（一次性）**，之后视频在本地解密，不经过第三方。
2. **网页版粘贴链接（零安装）**
   - 在微信里点视频号分享 -> 复制链接，打开 `https://sph.litao.workers.dev/` 粘贴解析下载。
   - 优点：不装任何东西。缺点：链接有时效、解析走第三方服务。
3. **微信小程序机器人（零安装）**
   - 小鸟下载助手 / 熊猫下载助手等：把视频号转发给机器人，它回传下载卡片。
   - 缺点：内容要经过第三方 bot。

### 某账号主页批量下载
- 推荐工具：`ltaoo/wx_channels_download`（GitHub，2025-10 仍在活跃发版）
  或 Gitee `rodert/WeixinVideoDownload`（明确支持"主页批量下载、按作者自动分类"）。
- 通用流程：安装工具并信任其本地根证书（一次性）→ 微信内打开该作者主页
  → 工具拦截主页信息流接口并列出全部视频 → 批量下载 → 拷入 `./videos/`。
- 注意：这类工具靠注入/代理实现，微信版本更新后可能失效，优先选活跃维护的项目。

> ⚠️ 版权提醒：视频号内容受原作者版权保护，下载请仅用于**个人收藏/学习**，
> 不要二次剪辑发布或传播。本工具同理。
> ⚠️ 隐私提醒：网页解析/小程序机器人方案内容经过第三方服务器，隐私敏感内容避免使用。

把下载好的 mp4 放到一个文件夹，例如 `./video/`（或 `./videos/`）。

---

## 第二步：运行提取脚本

```powershell
# 纯画面视频(主力场景): 抽帧 + 去重 + 关键帧带时间戳, 跳过语音转写
.venv\Scripts\python.exe process_video.py -i ./video --no-transcribe

# 有旁白的视频: 转写语音(faster-whisper, 首次会下载模型权重)
.venv\Scripts\python.exe process_video.py -i ./video

# 单文件 / 控制每视频最多关键帧数(滚动字幕型长视频用)
.venv\Scripts\python.exe process_video.py -i 某个视频.mp4 --no-transcribe --max-frames 30
```

参数：
- `-i/--input`：视频文件或文件夹（必填）
- `--fps`：抽帧频率，默认 1（每秒 1 张）
- `--diff`：关键帧阈值，默认 40（越大保留越少帧）
- `--max-frames`：单个视频最多保留多少张，超出则按时间均匀抽样（默认 40，防长视频爆量）
- `--no-transcribe`：跳过 Whisper 转写（纯画面视频用）
- `--model`：Whisper 模型，默认 `small`

输出结构：
```
output/  (本仓库真实数据在 output_videos/)
  视频名/
    frames/        # 去重后的关键帧 jpg, 文件名带时间戳: frame_0001_t00m12s.jpg
    raw_extract.md # 汇总: 源文件名 + 关键帧清单(含 mm:ss 时间戳列)
```

关键帧文件名末尾的 `t00m12s` 即该帧在视频中的位置（分/秒），
`raw_extract.md` 的帧清单也带 `mm:ss` 时间戳列，最终笔记可据此定位回看视频。

### 2.5 把关键帧变成文字（OCR）—— 本仓库目前的"读图"替代

> 当前运行环境的多模态读图能力不可用，所以"读关键帧"这一步改用本地 OCR。
> 画面里的文字被识别成文本后，再据此整理知识点。

```powershell
# 给 output_videos/ 下所有关键帧做中文 OCR, 产出每个视频目录的 ocr.md
.venv\Scripts\python.exe ocr_frames.py -i ./output_videos
```

- `ocr.md` 内容：每帧一行，带时间戳和该帧画面文字（按版面聚类还原阅读顺序）。
- 依赖 `rapidocr-onnxruntime`（模型随包自带，无需联网下载模型）。
- 识别重点是中文讲解句；代码/英文画面噪声较大，整理笔记时按需取舍。

---

## 第三步：交给我生成知识点 Markdown（标准操作）

把 `output/<视频名>/ocr.md`（以及可选的关键帧/转写）给我，我会：
1. 读 `ocr.md`，提取画面里的文字、图表、要点（配合视频文件名里的文案）；
2. 结合转写文本（若有）；
3. 整理成结构化 Markdown（标题层级 + 要点列表 + 关键概念 + 时间戳）。

> 注：若运行环境支持多模态读图，则直接读 `frames/` 关键帧即可，跳过上面 2.5 的 OCR。
> 当前环境不支持读图，故走 OCR 文字通道。

整理好的笔记（一篇 Markdown）放进对应视频目录，用归档脚本入库：

```powershell
# 归档一篇笔记到 notes/YYYY-MM/ 并刷新索引(默认移动原文件)
.venv\Scripts\python.exe archive_note.py -i ./output_videos/045_.../笔记.md --source-video video

# 常用参数: --summary "一句话总结" --date 2026-10-23 --keep 保留原文件
# 批量归档某目录下所有 笔记.md: 见第四步
# 手工改过笔记 front-matter 后, 只刷新索引:
.venv\Scripts\python.exe archive_note.py --reindex
```

归档约定：
```
notes/
  2026-10/
    <标题>.md        # front-matter 含 title/date/source_video/timestamps 等
```

批量归档整个 `output_videos/` 下所有 `笔记.md`：
```powershell
Get-ChildItem output_videos -Recurse -Filter 笔记.md | ForEach-Object {
  .venv\Scripts\python.exe archive_note.py -i $_.FullName --source-video video --date 2026-10-23
}
```
  INDEX.md           # 自动生成的索引: 日期 | 标题 | 一句话总结 | 来源视频
```

---

## 在本机安装并运行

本机已具备：Python 3.12（winget 安装）+ 项目虚拟环境 `.venv`（已装 opencv/pillow/numpy）。

```powershell
# 日常使用直接用 .venv 里的 python, 例如:
.venv\Scripts\python.exe process_video.py -i ./videos --no-transcribe
```

如需在新机器重建环境：

1. 安装 Python 3.12+（`winget install Python.Python.3.12`）。
2. 创建虚拟环境并安装依赖：
   ```powershell
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. 按"第二步"运行 `process_video.py`，把输出目录交给我生成 Markdown，再按"第三步"归档。

## 依赖与故障排查

- `opencv-python-headless`：抽帧（已内置 ffmpeg，无需单独装）
- `faster-whisper`：语音转写（首次运行会下载模型权重，需联网）
- `pillow`：仅生成测试视频 `gen_test_video.py` 需要
- 若 `faster-whisper` 装不上：纯画面视频本就不依赖它，直接加 `--no-transcribe` 即可。
- 抽帧失败：确认文件是正常 mp4，且 opencv 安装成功（`python -c "import cv2"`）。
