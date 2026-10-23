#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成一个用于端到端验证的测试视频: 含中文文字 + 简单图形(模拟"信息在画面"的知识视频)。
用法: python gen_test_video.py
输出: ./sample/test_video.mp4
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import cv2

W, H = 640, 360
FPS = 10
FRAMES_PER_SCENE = 15  # 每屏约 1.5 秒


def find_cjk_font():
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def make_frame(scene):
    font_path = find_cjk_font()
    title_font = ImageFont.truetype(font_path, 34) if font_path else ImageFont.load_default()
    body_font = ImageFont.truetype(font_path, 26) if font_path else ImageFont.load_default()

    img = Image.new("RGB", (W, H), scene["bg"])
    d = ImageDraw.Draw(img)
    d.text((30, 24), scene["title"], font=title_font, fill=scene["fg"])
    y = 90
    for line in scene["body"]:
        d.text((30, y), line, font=body_font, fill=scene["fg"])
        y += 46
    # 简单"图示": 矩形 + 圆, 模拟图表
    d.rectangle([410, 70, 600, 300], outline=scene["fg"], width=3)
    d.ellipse([450, 110, 560, 250], outline=scene["fg"], width=3)
    d.line([410, 300, 600, 70], fill=scene["fg"], width=2)

    arr = np.array(img)
    return arr[:, :, ::-1].copy()  # RGB -> BGR


def main():
    scenes = [
        {"bg": (245, 245, 245), "fg": (20, 20, 20),
         "title": "高效阅读三原则", "body": ["1. 主动预测", "2. 间隔回顾", "3. 输出倒逼输入"]},
        {"bg": (230, 240, 255), "fg": (10, 40, 90),
         "title": "原则一: 主动预测", "body": ["读前先猜结论", "带着问题去读"]},
        {"bg": (235, 255, 235), "fg": (10, 70, 30),
         "title": "原则二: 间隔回顾", "body": ["当天 / 隔天 / 周末", "对抗遗忘曲线"]},
        {"bg": (255, 245, 230), "fg": (90, 50, 10),
         "title": "原则三: 输出倒逼", "body": ["讲给别人听", "写卡片笔记"]},
        {"bg": (240, 230, 255), "fg": (50, 20, 90),
         "title": "小结", "body": ["预测 + 回顾 + 输出", "形成阅读闭环"]},
    ]
    out_dir = Path("sample")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "test_video.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vw = cv2.VideoWriter(str(out_path), fourcc, FPS, (W, H))
    for scene in scenes:
        frame = make_frame(scene)
        for _ in range(FRAMES_PER_SCENE):
            vw.write(frame)
    vw.release()
    print(f"已生成测试视频: {out_path}  ({len(scenes)*FRAMES_PER_SCENE} 帧)")


if __name__ == "__main__":
    from pathlib import Path
    main()
