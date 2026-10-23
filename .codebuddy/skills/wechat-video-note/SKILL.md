---
name: wechat-video-note
description: 处理微信视频号内容 -> 知识点 Markdown -> 归档到 notes/ -> 提交 GitHub。当用户要新增/处理微信视频笔记、根据 ocr.md 生成结构化笔记、批量归档或推送知识库时触发。
---

# 微信视频 -> 知识点笔记

本项目把微信视频号内容转成可检索的知识点 Markdown。脚本链路已经就绪：
- `process_video.py` 抽帧 + 帧间差异去重（+ 可选 Whisper 语音转写）
- `ocr_frames.py` 关键帧中文 OCR -> 每个视频目录的 `ocr.md`
- `archive_note.py` 归档到 `notes/YYYY-MM/` + 刷新 `notes/INDEX.md`

## 前置条件（确认已满足）
- 新视频已放进 `./video/incoming/`（已处理的在 `./video/done/`，不要混放）。
- 已抽帧 + OCR：`output_videos/<serial>_.../` 下含 `frames/` + `ocr.md`。
- **当前环境无多模态读图能力，必须走 OCR 文字通道，不要尝试读图。**

## 生成一篇笔记的标准动作
1. 用 PowerShell 去重读取该视频的 `ocr.md`（避免长视频原文超长被截断）：
   ```powershell
   cd d:\Project\wechat-knowledge
   $d = Get-ChildItem output_videos -Directory | Where-Object { $_.Name -like "<serial>_*" } | Select-Object -First 1
   $seen = @{}
   Get-Content "$($d.FullName)\ocr.md" -Encoding UTF8 | ForEach-Object {
     if($_ -match '\|\s*`[^`]*`\s*\|\s*(.+?)\s*\|'){
       $t = $Matches[1]
       if(-not $seen.ContainsKey($t)){ $seen[$t]=1; Write-Host "  - $t" }
     }
   }
   ```
   一批只处理 3~5 个编号；超长视频（如 30 帧技能清单）单独处理。
2. 结合视频目录名里的文案，整理成结构化 Markdown，存为 `output_videos/<dir>/笔记.md`。
   格式（务必与已有 50 篇一致）：
   - 顶部引用块：来源（微信视频号《标题》）、提取方式、日期。
   - `## 一句话总结`
   - `## 核心要点`（分点，含具体数据/项目名/Star 数/命令）
   - `## 展开说明`（含与其他笔记的交叉引用）
   - `## 时间戳索引`（表格：时间 | 画面内容，时间取自 `ocr.md`/帧文件名）
3. 归档（带 `--frames-dir` 以正确推断关键帧时间戳）：
   ```powershell
   $dir = "<output_videos 下该视频目录的绝对路径>"
   .venv\Scripts\python.exe archive_note.py -i "$dir\笔记.md" --source-video video --frames-dir "$dir\frames" --date 2026-10-23
   ```
4. 全部完成后提交 GitHub：
   ```powershell
   git add -A
   git commit -m "新增/更新微信视频知识点笔记"
   git push
   ```
   （若 `git` 不在 PATH，用完整路径 `C:\Program Files\Git\cmd\git.exe`。提交邮箱用 `dolanshu@users.noreply.github.com`。）

## 批量归档
```powershell
Get-ChildItem output_videos -Recurse -Filter 笔记.md | ForEach-Object {
  $dir = $_.Directory.FullName
  .venv\Scripts\python.exe archive_note.py -i $_.FullName --source-video video --frames-dir "$dir\frames" --date 2026-10-23
}
```

## 注意事项
- `.gitignore` 已排除 `video/ output/ output_videos/ .venv/`，只入库代码/笔记/文档；**不要** `git add` 这些大目录。
- 新视频只放 `./video/incoming/`；处理完归档后，把 incoming 里的源移到 `./video/done/`，保持 incoming 为空（它就是"是否有新视频"的判据）。
- `ocr_frames.py` 对已有 `ocr.md` 的目录自动跳过，重复跑安全（只 OCR 新增）。
- 重复下载的视频（如 020/021、023/024/025）只做一份。
- `pending_notes.md` 是 59 篇分类勾选清单，可据此跟踪进度；未勾选的非技术/低价值内容可跳过。
- PowerShell 变量插值写 `${n}_*`，不要写 `$n_*`。
- OCR 对中文讲解句可靠，代码/英文画面噪声大，整理时按需取舍。
