#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信视频 -> 知识点素材 提取流水线 v1
=====================================

流程:
  1. 抽帧: 用 opencv 按 fps 抽取视频帧, 并用帧间差异做轻量去重, 只保留"关键帧"
  2. 转写: 可选, 用 faster-whisper 把音频转成文字 (无旁白视频用 --no-transcribe)
  3. 汇总: 输出 raw_extract.md (列出关键帧路径 + 转写文本), 供后续生成知识点 Markdown

为什么这样设计:
  - 你这类视频很多"信息在画面里、没有语音", 所以抽帧是主通道, 转写是可选副通道
  - 1fps 抽出来的帧大量重复, 用帧间 MSE 去重后只留真正变化的画面, 数量可控
  - 去重后的关键帧 + 转写文本, 交给(多模态的)我来读图+理解, 产出知识点 Markdown

用法:
  python process_video.py -i video.mp4
  python process_video.py -i ./videos --fps 1 --no-transcribe
  python process_video.py -i video.mp4 --model small --lang zh
"""
import argparse
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

try:
    import cv2
except ImportError:
    print("[错误] 未安装 opencv-python-headless, 请先: pip install opencv-python-headless")
    sys.exit(1)

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv", ".m4v"}


def iter_videos(input_path: Path):
    if input_path.is_file():
        if input_path.suffix.lower() in VIDEO_EXTS:
            yield input_path
    else:
        for p in sorted(input_path.rglob("*")):
            if p.is_file() and p.suffix.lower() in VIDEO_EXTS:
                yield p


def fmt_ts(seconds: float) -> str:
    """秒 -> mm:ss (用于笔记里的时间戳链接)。"""
    seconds = max(0.0, float(seconds))
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"


def fmt_ts_filename(seconds: float) -> str:
    """秒 -> t00m12s (用于帧文件名, 避免冒号在 Windows 上非法)。"""
    seconds = max(0.0, float(seconds))
    return f"t{int(seconds // 60):02d}m{int(seconds % 60):02d}s"


def save_jpg(frame, path: Path):
    """写 jpg: 用 imencode + Python 写文件, 避开 cv2.imwrite 不支持非 ASCII 路径的问题。"""
    ok, buf = cv2.imencode(".jpg", frame)
    if not ok:
        return False
    with open(path, "wb") as f:
        f.write(buf.tobytes())
    return True


def open_ascii_copy(video_path: Path):
    """Windows 上 OpenCV 打不开含中文/emoji 的路径, 需要时复制到 ASCII 临时文件。

    返回 (实际使用的路径, 临时文件对象或 None)。
    """
    try:
        str(video_path).encode("ascii")
        return video_path, None
    except UnicodeEncodeError:
        tmp_dir = Path(tempfile.gettempdir())
        tmp = tmp_dir / f"wk_{uuid.uuid4().hex}{video_path.suffix.lower()}"
        shutil.copy2(video_path, tmp)
        return tmp, tmp


def extract_key_frames(video_path: Path, out_dir: Path, fps: float, diff_threshold: float,
                       max_frames: int = 40):
    """按 fps 抽帧, 用帧间 MSE 去重, 只保留画面变化足够大的关键帧。

    返回 [(帧路径, 该帧在视频中的秒数), ...], 时间戳 = 解码帧号 / video_fps,
    这样最终笔记可以带 "00:12" 之类的定位信息。

    max_frames: 单个视频最多保留多少张。滚动字幕/长视频画面一直在变,
    单纯调高阈值压不下来, 超过上限时按时间均匀抽样, 保证覆盖整段视频。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    real_path, tmp = open_ascii_copy(video_path)
    cap = cv2.VideoCapture(str(real_path))
    if not cap.isOpened():
        print(f"  [跳过] 无法打开视频: {video_path}")
        if tmp:
            tmp.unlink(missing_ok=True)
        return []
    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    interval = max(1, int(round(video_fps / fps)))  # 每隔多少帧抽一张
    last_gray = None
    idx = 0
    candidates = []  # [(秒数, jpg字节), ...]
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_small = cv2.resize(gray, (64, 64))
            if last_gray is None:
                keep = True
            else:
                mse = ((gray_small.astype("float32") - last_gray.astype("float32")) ** 2).mean()
                keep = mse > diff_threshold
            if keep:
                ok, buf = cv2.imencode(".jpg", frame)
                if ok:
                    candidates.append((idx / video_fps, buf.tobytes()))
                    last_gray = gray_small
        idx += 1
    cap.release()
    if tmp:
        tmp.unlink(missing_ok=True)

    if max_frames and len(candidates) > max_frames:
        step = len(candidates) / max_frames
        picked = [candidates[min(len(candidates) - 1, int(i * step))] for i in range(max_frames)]
        note = f"(候选 {len(candidates)} 张, 均匀抽样到 {max_frames} 张)"
    else:
        picked = candidates
        note = ""

    saved = []
    for i, (t, data) in enumerate(picked):
        fname = f"frame_{i:04d}_{fmt_ts_filename(t)}.jpg"
        with open(out_dir / fname, "wb") as f:
            f.write(data)
        saved.append((out_dir / fname, t))
    print(f"  [抽帧] {video_path.name[:30]}...: 总帧 {total}, "
          f"关键帧 {len(saved)} 张 {note}")
    return saved


def transcribe(video_path: Path, model_size: str, language: str, compute_type: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("  [转写] 未安装 faster-whisper, 跳过 (pip install faster-whisper)")
        return None
    print(f"  [转写] 加载 Whisper 模型 {model_size} (首次会下载权重)...")
    model = WhisperModel(model_size, device="cpu", compute_type=compute_type)
    segments, info = model.transcribe(
        str(video_path), language=language, beam_size=5, vad_filter=True
    )
    texts = [f"[{seg.start:.1f}s] {seg.text.strip()}" for seg in segments]
    print(f"  [转写] 完成, 检测语言: {info.language}")
    return "\n".join(texts)


def write_raw(out_dir: Path, name: str, frames, transcript, source_name: str = ""):
    md = out_dir / "raw_extract.md"
    lines = [f"# 素材提取: {name}", ""]
    if source_name:
        lines += [f"- 源视频文件: `{source_name}`", ""]
    if transcript:
        lines += ["## 语音转写", "", "```text", transcript, "```", ""]
    else:
        lines += ["## 语音转写", "",
                  "_(本视频无旁白或已跳过转写; 知识点来自下方关键帧)_", ""]
    lines += ["## 关键帧", "",
              f"共 {len(frames)} 张, 位于 `{out_dir}/frames/` 目录 "
              "(文件名末尾的 t00m12s 即该帧在视频中的时间):", "",
              "| 时间戳 | 帧文件 |", "|---|---|"]
    for f, t in frames:
        lines.append(f"| `{fmt_ts(t)}` | `{f.name}` |")
    md.write_text("\n".join(lines), encoding="utf-8")
    return md


def safe_stem(video_path: Path, maxlen: int = 40) -> str:
    """输出目录名: 视频名可能是一整段文案(很长且含非法字符), 截断 + 清洗后使用。"""
    s = re.sub(r"[\\\/\:\*\?\"\<\>\|]+", " ", video_path.stem).strip()
    s = re.sub(r"\s+", "_", s)
    return (s[:maxlen].rstrip("_.") or "video")


def process(video_path, base_out, fps, diff_threshold, do_transcribe,
           model_size, language, compute_type, serial: int = 0, max_frames: int = 40):
    name = f"{serial:03d}_{safe_stem(video_path)}"
    out_dir = base_out / name
    frames_dir = out_dir / "frames"
    print(f"\n=== 处理: {video_path.name} ===")
    frames = extract_key_frames(video_path, frames_dir, fps, diff_threshold, max_frames)
    transcript = None
    if do_transcribe:
        transcript = transcribe(video_path, model_size, language, compute_type)
    md = write_raw(out_dir, video_path.stem[:60], frames, transcript, video_path.name)
    print(f"  [完成] 原始素材已汇总: {md}")
    return md


def main():
    ap = argparse.ArgumentParser(description="微信视频 -> 知识点素材提取")
    ap.add_argument("-i", "--input", required=True, help="视频文件或包含视频的文件夹")
    ap.add_argument("-o", "--output", default="./output", help="输出根目录")
    ap.add_argument("--fps", type=float, default=1.0, help="抽帧频率(每秒帧数), 默认1")
    ap.add_argument("--diff", type=float, default=40.0,
                    help="关键帧判定阈值(MSE), 越大越严格/保留越少帧")
    ap.add_argument("--max-frames", type=int, default=40,
                    help="单个视频最多保留多少张关键帧(超出则按时间均匀抽样), 默认40")
    ap.add_argument("--no-transcribe", action="store_true",
                    help="跳过语音转写(纯画面视频用)")
    ap.add_argument("--model", default="small", help="Whisper 模型, 默认 small")
    ap.add_argument("--lang", default="zh", help="转写语言, 默认 zh")
    ap.add_argument("--compute-type", default="int8", help="Whisper 精度, CPU 用 int8")
    args = ap.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f"[错误] 路径不存在: {input_path}")
        sys.exit(1)
    base_out = Path(args.output).expanduser().resolve()
    base_out.mkdir(parents=True, exist_ok=True)

    videos = list(iter_videos(input_path))
    if not videos:
        print("[错误] 未找到任何视频文件")
        sys.exit(1)
    print(f"找到 {len(videos)} 个视频")
    for i, v in enumerate(videos, 1):
        process(v, base_out, args.fps, args.diff, not args.no_transcribe,
                args.model, args.lang, args.compute_type, serial=i,
                max_frames=args.max_frames)
    print("\n全部处理完成。把 output/<视频名>/ 目录(关键帧+raw_extract.md)发给我, "
          "我来读图并生成知识点 Markdown。")


if __name__ == "__main__":
    # Windows 控制台默认 GBK, 视频名里的 emoji/生僻字会让 print 抛异常
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
