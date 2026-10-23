#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键帧 -> 画面文字 (OCR)
=======================

给 output/<视频>/frames/ 里的关键帧做中文 OCR, 产出 ocr.md:
每帧一行, 带时间戳和该帧画面里识别到的文字(按版面分行合并)。

为什么要这一步: 视频号的知识类视频"信息在画面里", 把画面文字转成文本后,
才能在没有读图能力的环境里继续整理知识点笔记。

用法:
  python ocr_frames.py                       # 处理 output_videos/ 下所有视频目录
  python ocr_frames.py -i ./output_videos --limit 10
  python ocr_frames.py --dir 001 --force     # 只重跑某个目录
"""
import argparse
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    # 本机缺 VC++ 运行库, msvc-runtime 把 DLL 装在 venv/Scripts 下, 需显式注册
    for d in {Path(sys.executable).parent, Path(sys.prefix) / "Scripts"}:
        if d.is_dir():
            try:
                os.add_dll_directory(str(d))
            except Exception:
                pass


def load_engine():
    from rapidocr_onnxruntime import RapidOCR
    return RapidOCR()


def lines_from_result(result, y_tol: int = 18):
    """把 OCR 的文本框按 y 聚类成行, 行内按 x 排序, 还原阅读顺序。"""
    if not result:
        return []
    items = []
    for box, text, score in result:
        text = (text or "").strip()
        if not text:
            continue
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        items.append({"y": sum(ys) / len(ys), "x": min(xs), "text": text})
    items.sort(key=lambda it: (it["y"], it["x"]))
    rows, cur = [], [items[0]]
    for it in items[1:]:
        if abs(it["y"] - cur[-1]["y"]) <= y_tol:
            cur.append(it)
        else:
            rows.append(cur)
            cur = [it]
    rows.append(cur)
    return [" ".join(i["text"] for i in sorted(r, key=lambda t: t["x"])) for r in rows]


def parse_ts(name: str) -> str:
    import re
    m = re.search(r"_t(\d{2})m(\d{2})s$", Path(name).stem)
    return f"{m.group(1)}:{m.group(2)}" if m else "??:??"


def main():
    ap = argparse.ArgumentParser(description="关键帧 OCR -> ocr.md")
    ap.add_argument("-i", "--input", default="./output_videos", help="抽帧输出根目录")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个视频目录(调试用)")
    ap.add_argument("--dir", help="只处理名字包含该串的视频目录")
    ap.add_argument("--force", action="store_true", help="已有 ocr.md 也重跑")
    args = ap.parse_args()

    root = Path(args.input).expanduser().resolve()
    if not root.is_dir():
        print(f"[错误] 目录不存在: {root}")
        sys.exit(1)

    dirs = sorted(d for d in root.iterdir() if d.is_dir() and (d / "frames").is_dir())
    if args.dir:
        dirs = [d for d in dirs if args.dir in d.name]
    if args.limit:
        dirs = dirs[:args.limit]

    engine = load_engine()
    print(f"OCR 引擎就绪, 待处理 {len(dirs)} 个视频目录")

    for i, d in enumerate(dirs, 1):
        out_md = d / "ocr.md"
        if out_md.exists() and not args.force:
            print(f"[{i}/{len(dirs)}] 跳过(已有 ocr.md): {d.name}", flush=True)
            continue
        raw = d / "raw_extract.md"
        source = ""
        if raw.exists():
            for line in raw.read_text(encoding="utf-8").splitlines():
                if line.startswith("- 源视频文件:"):
                    source = line.split(":", 1)[1].strip().strip("`")
                    break
        frames = sorted((d / "frames").glob("*.jpg"))
        print(f"[{i}/{len(dirs)}] 开始 OCR: {d.name} ({len(frames)} 帧)", flush=True)
        rows = []
        for j, f in enumerate(frames, 1):
            try:
                result, _ = engine(str(f))
            except Exception as e:
                print(f"    [{j}/{len(frames)}] OCR失败 {f.name}: {e}", flush=True)
                result = None
            lines = lines_from_result(result)
            if lines:
                rows.append((parse_ts(f.name), f.name, " ／ ".join(lines)))
            if j % 5 == 0:
                print(f"    [{j}/{len(frames)}] ...", flush=True)
        body = [f"# 画面文字 OCR: {d.name}", ""]
        if source:
            body += [f"- 源视频: `{source}`", ""]
        body += [f"共 {len(frames)} 帧, 其中 {len(rows)} 帧识别到文字。", "",
                 "| 时间 | 文字 |", "|---|---|"]
        for ts, fname, text in rows:
            body.append(f"| `{ts}` | {text} |")
        out_md.write_text("\n".join(body) + "\n", encoding="utf-8")
        print(f"[{i}/{len(dirs)}] 完成 {d.name}: {len(rows)}/{len(frames)} 帧有文字 -> ocr.md", flush=True)

    print("\nOCR 完成。", flush=True)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
