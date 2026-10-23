# 微信视频 -> 知识点 Markdown 提取工具

把你在微信里"转发给自己"的视频号内容，自动提取成可检索的知识点 Markdown。

## 整体流程

```
视频号视频
  └─ 下载器（一键 / 网页 / 机器人） -> mp4 文件  (./video/incoming/)
        ├─ process_video.py 抽帧 + 去重  -> 关键帧 (画面文字/图表)   ← 主通道
        └─ process_video.py Whisper 转写 -> 语音文字 (有旁白才用)
              ↓
        ocr_frames.py 关键帧中文 OCR -> ocr.md   ← 当前环境的"读图"替代
              ↓ 把 ocr.md 给我
          我(读 OCR 文本)整理 -> 知识点 Markdown (笔记.md)
              ↓
          archive_note.py 归档 -> notes/YYYY-MM/ + 刷新 INDEX.md
              ↓
          git commit + push -> GitHub 知识库
```

设计要点：你这类视频很多"信息在画面里、没有语音"，所以**抽帧是主通道**；
抽出来的帧用帧间差异去重，只留真正变化的"关键帧"。**当前运行环境无多模态读图能力**，
因此"读关键帧"改用本地 OCR 取文字，再据文字整理笔记（见 §2.5）。

---

## 当前进度（2026-10-23）

- **原 59 个视频已抽帧 + OCR**（`output_videos/<serial>_.../` 每目录含 `frames/` + `raw_extract.md` + `ocr.md`）；源视频已归入 `video/done/`，后续新视频放 `video/incoming/`。
- **50 篇笔记已归档**到 `notes/2026-10/`（含首轮 4 篇 + 测试示例；本轮用户勾选生成 45 篇）。
- **已清理**：未勾选的 `023/024/025/026/011/044` 已从 `pending_notes.md` 移除并删除源视频与抽帧产物；`021` 为已勾选但属 `020` 的重复变体，未单独做（`020` 已覆盖其知识点）。
- 已入库：`notes/INDEX.md` 含全部索引；大体积素材按 `.gitignore` 排除，只上传代码/脚本/笔记/文档。

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
  → 工具拦截主页信息流接口并列出全部视频 → 批量下载 → 拷入 `./video/`。

> ⚠️ 版权提醒：视频号内容受原作者版权保护，下载请仅用于**个人收藏/学习**，不要二次剪辑发布或传播。
> ⚠️ 隐私提醒：网页解析/小程序机器人方案内容经过第三方服务器，隐私敏感内容避免使用。

把下载好的 mp4 放到 `./video/incoming/`。

> 📁 **目录约定（怎么知道哪个是新视频）**：`./video/` 下分两个子目录——
> - `video/incoming/`：**你只往这里丢新视频**。它非空 = 有未处理的新视频（唯一判据，不用记、不用遍历）。
> - `video/done/`：已抽帧+OCR+归档的视频源，处理完自动移入。

---

## 第二步：抽帧 + OCR

```powershell
# 1) 抽帧 + 去重 + 关键帧带时间戳, 跳过语音转写(主力场景); 只扫 incoming
.venv\Scripts\python.exe process_video.py -i ./video/incoming --no-transcribe

# 2) 给 output_videos/ 下所有关键帧做中文 OCR; 已有 ocr.md 的目录自动跳过(幂等), 只对新增的做
.venv\Scripts\python.exe ocr_frames.py -i ./output_videos
```

参数（`process_video.py`）：
- `-i/--input`：视频文件或文件夹（必填）
- `--fps`：抽帧频率，默认 1（每秒 1 张）
- `--diff`：关键帧阈值，默认 40（越大保留越少帧）
- `--max-frames`：单个视频最多保留多少张，超出则按时间均匀抽样（默认 40，防长视频爆量）
- `--no-transcribe`：跳过 Whisper 转写（纯画面视频用）
- `--model`：Whisper 模型，默认 `small`

输出结构（`output_videos/`，真实数据在此，非 `output/`）：
```
output_videos/
  <serial>_视频文案/
    frames/        # 去重后的关键帧 jpg, 文件名带时间戳: frame_0001_t00m12s.jpg
    raw_extract.md # 汇总: 源文件名 + 关键帧清单(含 mm:ss 时间戳列)
    ocr.md         # 每帧一行: 时间戳 + 画面文字(按版面聚类还原阅读顺序)
```

关键帧文件名末尾的 `t00m12s` 即该帧位置（分/秒），`raw_extract.md`/`ocr.md` 均带时间戳，笔记可据此回看视频。

> OCR 依赖 `rapidocr-onnxruntime`（模型随包自带，无需联网）。识别重点是中文讲解句；
> 代码/英文画面噪声较大，整理笔记时按需取舍。若环境日后支持读图，可跳过 OCR 直接看 `frames/`。

---

## 第三步：生成知识点笔记（标准格式）

把 `output_videos/<dir>/ocr.md` 给我（或读下面"去重读取"命令的输出），我整理成一篇 `笔记.md` 放进同目录。

### 笔记格式规范（务必与已有 50 篇一致）
```markdown
# <标题，来自视频文件名文案，去掉话题标签>

> 来源：微信视频号《<原标题>》
> 提取方式：抽帧 → 画面 OCR → 整理
> 日期：2026-10-23

## 一句话总结
<用一句话说清这个视频讲了什么、核心价值>

## 核心要点
- <分点，含具体数据/项目名/Star 数/命令等硬信息>
- ...

## 展开说明
- <与其他笔记的交叉引用、适用场景、踩坑提醒等>

## 时间戳索引
| 时间 | 画面内容 |
|---|---|
| 00:00~ | ... |
```

> **GitHub 仓库引用规则**：笔记中出现的所有 GitHub 仓库（`owner/repo` 形式，如 `` `microsoft/markitdown` ``）一律渲染为可点击直连 `[owner/repo](https://github.com/owner/repo)`，方便跳转。已有 50 篇已用脚本批量补过此链接。

### 去重读取 OCR（避免长视频超长截断）
不要把整篇 `ocr.md` 原文一次性全部 dump（长视频会超出上下文被截断）。用下面命令只输出**去重后的唯一文字行**：
```powershell
cd d:\Project\wechat-knowledge
foreach($n in @('014','016','018')){   # 一批 3~5 个编号
  $d = Get-ChildItem output_videos -Directory | Where-Object { $_.Name -like "${n}_*" } | Select-Object -First 1
  if($d){
    Write-Host "`n##### $n #####"
    $seen = @{}
    Get-Content "$($d.FullName)\ocr.md" -Encoding UTF8 | ForEach-Object {
      if($_ -match '\|\s*`[^`]*`\s*\|\s*(.+?)\s*\|'){
        $t = $Matches[1]
        if(-not $seen.ContainsKey($t)){ $seen[$t]=1; Write-Host "  - $t" }
      }
    }
  }
}
```
> 注意 PowerShell 变量插值写 `${n}_*`，不要写 `$n_*`（会被解析成变量 `$n_`）。

---

## 第四步：归档到 notes/

```powershell
# 批量归档 output_videos/ 下所有 笔记.md (带 --frames-dir 以正确推断关键帧时间戳)
Get-ChildItem output_videos -Recurse -Filter 笔记.md | ForEach-Object {
  $dir = $_.Directory.FullName
  .venv\Scripts\python.exe archive_note.py -i $_.FullName --source-video video --frames-dir "$dir\frames" --date 2026-10-23
}
```
- 默认移动原 `笔记.md` 到 `notes/YYYY-MM/` 并刷新 `notes/INDEX.md`。
- 单篇：`archive_note.py -i <path> --source-video video --frames-dir <dir>\frames --date 2026-10-23`
- 只刷新索引（手工改过 front-matter 后）：`archive_note.py --reindex`

---

## 第五步：提交到 GitHub

仓库 `git@github.com:dolanshu/wechat-knowledge.git`，分支 `main`，已配 SSH key。
（若 `git` 不在 PATH，用完整路径 `C:\Program Files\Git\cmd\git.exe` 代替下面的 `git`。）

```powershell
git add -A
git commit -m "描述本次新增/修改的笔记"
git push
```
- 提交身份邮箱用 GitHub noreply：`dolanshu@users.noreply.github.com`（已配置）。
- `.gitignore` 已排除 `video/ output/ output_videos/ .venv/ sample/test_video.mp4`，只上传代码/脚本/笔记/文档。

---

## 后续更新指南（新增一个视频的标准动作）

**判据**：`video/incoming/` 里有没有文件，就是"有没有新视频要处理"的唯一信号。平时它是空的。
（`.gitignore` 已排除 `video/`，这些源文件不进 GitHub，仅本地留存。）

1. **下载**视频 → 丢进 `./video/incoming/`（重复下载的变体只留一份）。
2. **抽帧 + OCR**（只扫 incoming，OCR 自动跳过已处理的目录）：
   ```powershell
   .venv\Scripts\python.exe process_video.py -i ./video/incoming --no-transcribe
   .venv\Scripts\python.exe ocr_frames.py -i ./output_videos   # 幂等: 只 OCR 新增目录
   ```
3. **生成笔记**：用 §3 去重读取命令取素材，按格式写 `笔记.md` 到对应 `output_videos/<dir>/`。
4. **归档**：§4 批量归档（带 `--frames-dir`）。
5. **收尾**：把 `video/incoming/` 里已处理的源视频移到 `video/done/`，保持 incoming 干净。
6. **入库**：§5 `git add -A && git commit && git push`。

> 重复视频、非技术/低价值内容可跳过；`pending_notes.md` 是早期 59 篇的分类勾选清单（历史参考），新视频无需再登记它。

---

## 本项目的 Skill

已沉淀 CodeBuddy skill：`.codebuddy/skills/wechat-video-note/SKILL.md`，
把"生成笔记 + 归档 + 入库"的流程与格式规范固化，后续会话处理新视频时可直接触发，
无需每次重新解释上下文。

---

## 在本机安装并运行

本机已具备：Python 3.12（winget 安装）+ 项目虚拟环境 `.venv`（已装 opencv/pillow/numpy/faster-whisper/rapidocr-onnxruntime）。

```powershell
# 日常使用直接用 .venv 里的 python
.venv\Scripts\python.exe process_video.py -i ./video/incoming --no-transcribe
```

如需在新机器重建环境：
1. 安装 Python 3.12+（`winget install Python.Python.3.12`）。
2. 创建虚拟环境并安装依赖：
   ```powershell
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

## 依赖与故障排查

- `opencv-python-headless`：抽帧（已内置 ffmpeg，无需单独装）
- `faster-whisper`：语音转写（首次运行会下载模型权重，需联网）
- `pillow`：仅生成测试视频 `gen_test_video.py` 需要
- `rapidocr-onnxruntime`：关键帧 OCR（模型随包自带）
- 若 `faster-whisper` 装不上：纯画面视频本就不依赖它，直接加 `--no-transcribe`。
- 抽帧失败：确认文件是正常 mp4，且 opencv 安装成功（`python -c "import cv2"`）。
- Windows 非 ASCII 路径/GBK 控制台：脚本已做兼容（临时拷 ASCII 副本 + imencode 写文件 + UTF-8 输出）。
- 长视频爆量：用 `--max-frames 30` 控制每视频最多关键帧数。
