#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识点笔记归档器 (P4)
=====================

把已经生成好的知识点 Markdown 归档进知识库, 并刷新索引。

约定:
  notes/YYYY-MM/<标题>.md     归档位置(按月份分目录)
  notes/INDEX.md              索引(标题 + 一句话总结 + 来源), 自动重建

front-matter 字段:
  title / date / source_video / source_frames / timestamps / tags

用法:
  # 归档一篇(默认移动到 notes/2026-10/)
  python archive_note.py -i ./output/test_video/note.md --source-video sample/test_video.mp4

  # 指定日期/总结, 保留原文件
  python archive_note.py -i note.md --date 2026-10-22 --summary "预测→回顾→输出" --keep

  # 只重建索引(比如手工改过笔记的 front-matter)
  python archive_note.py --reindex
"""
import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

NOTES_DIR = Path("notes")
INDEX_FILE = NOTES_DIR / "INDEX.md"
FM_RE = re.compile(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.S)


def slugify(title: str) -> str:
    """标题 -> 安全文件名(保留中文/字母数字)。"""
    s = re.sub(r"[\\\/\:\*\?\"\<\>\|]", " ", title)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"[^\w\u4e00-\u9fff\-\.]", "", s)
    return (s.strip("-") or "note")[:60]


def parse_front_matter(text: str):
    """返回 (front_matter字典, 正文)。没有 front-matter 时字典为空。"""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip("'\"")
    return fm, text[m.end():]


def render_front_matter(fields: dict) -> str:
    order = ["title", "date", "source_video", "source_frames", "timestamps", "tags"]
    lines = ["---"]
    for k in order:
        if k in fields:
            lines.append(f"{k}: {fields[k]}")
    for k in fields:
        if k not in order:
            lines.append(f"{k}: {fields[k]}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_summary_from_body(body: str) -> str:
    """当 front-matter 没有 summary 时, 从正文 `## 一句话总结` 段提取首段作为总结。"""
    in_sec = False
    buf = []
    for line in body.splitlines():
        s = line.strip()
        if re.match(r"^##\s*一句话总结\s*$", s):
            in_sec = True
            continue
        if in_sec:
            if re.match(r"^##\s", s):   # 遇到下一个二级标题就结束
                break
            if s:
                buf.append(s)
    if not buf:
        return ""
    text = " ".join(buf)
    text = re.sub(r"`([^`]*)`", r"\1", text)   # 去掉行内代码反引号, 保留内容
    text = re.sub(r"[*_#>]", "", text)          # 去掉加粗/斜体/引用等标记
    text = re.sub(r"\s+", " ", text).strip()
    return text[:200]


def list_timestamps(frames_dir: Path):
    """从关键帧目录读出 [时间戳 -> 帧文件] 列表。"""
    if not frames_dir.is_dir():
        return []
    items = []
    for p in sorted(frames_dir.glob("*.jpg")):
        m = re.search(r"_t(\d{2})m(\d{2})s$", p.stem)
        ts = f"{m.group(1)}:{m.group(2)}" if m else "??:??"
        items.append((ts, p.as_posix()))
    return items


def archive(note_path: Path, args):
    if not note_path.is_file():
        print(f"[错误] 笔记文件不存在: {note_path}")
        sys.exit(1)
    text = note_path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(text)

    title = args.title or fm.get("title") or first_heading(body) or note_path.stem
    d = args.date or fm.get("date") or date.today().isoformat()
    summary = args.summary or fm.get("summary") or extract_summary_from_body(body)

    fields = dict(fm)
    fields["title"] = title
    fields["date"] = d
    fields.setdefault("tags", "[]")
    if args.source_video or "source_video" not in fields:
        fields["source_video"] = args.source_video or fm.get("source_video", "")
    if summary:
        fields["summary"] = summary

    frames_dir = Path(args.frames_dir) if args.frames_dir else None
    if frames_dir is None and fields.get("source_frames"):
        frames_dir = Path(fields["source_frames"])
    if frames_dir is None and fields.get("source_video"):
        # 默认按流水线输出结构推断: output/<视频名>/frames/
        guess = Path("output") / Path(fields["source_video"]).stem / "frames"
        if guess.is_dir():
            frames_dir = guess
    if frames_dir and frames_dir.is_dir():
        fields["source_frames"] = frames_dir.as_posix()
        ts = list_timestamps(frames_dir)
        if ts:
            fields["timestamps"] = "[" + ", ".join(f"{t}" for t, _ in ts) + "]"

    month = d[:7]
    out_dir = NOTES_DIR / month
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (slugify(title) + ".md")
    out_path.write_text(render_front_matter(fields) + body.lstrip("\n"), encoding="utf-8")

    if args.keep:
        print(f"[归档] 已写入 {out_path} (保留原文件)")
    else:
        if note_path.resolve() != out_path.resolve():
            note_path.unlink()
        print(f"[归档] {note_path} -> {out_path}")
    return out_path


def read_note_meta(md: Path):
    fm, body = parse_front_matter(md.read_text(encoding="utf-8"))
    title = fm.get("title") or first_heading(body) or md.stem
    return {
        "title": title,
        "date": fm.get("date", ""),
        "summary": fm.get("summary") or extract_summary_from_body(body),
        "source": fm.get("source_video", ""),
        "rel": md.relative_to(NOTES_DIR).as_posix(),
    }


def reindex():
    if not NOTES_DIR.is_dir():
        print("[错误] 还没有 notes/ 目录, 先归档一篇笔记吧")
        sys.exit(1)
    notes = [p for p in sorted(NOTES_DIR.rglob("*.md")) if p.name != "INDEX.md"]
    metas = sorted((read_note_meta(p) for p in notes),
                   key=lambda m: m["date"], reverse=True)
    lines = [
        "# 知识点索引",
        "",
        f"> 由 `archive_note.py` 自动生成于 {date.today().isoformat()}。"
        "改了笔记的 front-matter 后重跑 `python archive_note.py --reindex` 即可刷新。",
        "",
        f"共 **{len(metas)}** 篇。",
        "",
        "| 日期 | 标题 | 一句话总结 | 来源视频 |",
        "|---|---|---|---|",
    ]
    for m in metas:
        lines.append(
            f"| {m['date']} | [{m['title']}]({m['rel']}) | {m['summary']} | {m['source']} |"
        )
    INDEX_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[索引] 已重建 {INDEX_FILE} (共 {len(metas)} 篇)")


def main():
    ap = argparse.ArgumentParser(description="知识点笔记归档 + 索引")
    ap.add_argument("-i", "--input", help="待归档的知识点 Markdown 文件")
    ap.add_argument("--title", help="标题(默认取 front-matter 或正文第一个 # 标题)")
    ap.add_argument("--date", help="日期 YYYY-MM-DD(默认今天)")
    ap.add_argument("--summary", help="一句话总结(写进 front-matter 与索引)")
    ap.add_argument("--source-video", help="来源视频路径")
    ap.add_argument("--frames-dir", help="关键帧目录, 用于生成时间戳链接")
    ap.add_argument("--keep", action="store_true", help="保留原文件(默认移动)")
    ap.add_argument("--reindex", action="store_true", help="只重建 notes/INDEX.md")
    args = ap.parse_args()

    if args.reindex or not args.input:
        if not args.input and not args.reindex:
            ap.error("需要 -i/--input 或 --reindex")
        reindex()
        return
    archive(Path(args.input).expanduser().resolve(), args)
    reindex()


if __name__ == "__main__":
    main()
