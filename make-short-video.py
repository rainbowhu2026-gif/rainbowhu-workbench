#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彩虹心理短视频生成器 v2.0
从文章标题+内容生成抖音竖版短视频(1080x1920)

改进:
- 去掉二维码, 聚焦涨粉
- ASS高级字幕: 3秒钩子开场 + 主字幕 + 关注CTA结尾
- 增强画面: 多层渐变 + 装饰图形 + 内容卡片 + 品牌水印
- TTS增加开头钩子和结尾关注引导
- 可选BGM支持
- 遵循ShortVideoForge六步SOP + 口播脚本工厂黄金3秒
"""

import asyncio
import edge_tts
import imageio_ffmpeg
import subprocess
import sys
import os
import math
import argparse
import shutil
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ============ CONFIG ============
WIDTH = 1080
HEIGHT = 1920
FPS = 30
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FONT_REGULAR = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+8%"
WORKSPACE = os.path.dirname(os.path.abspath(__file__))

# 5 color themes
THEMES = [
    {"name": "warm",   "top": (255, 94, 98),   "mid": (255, 138, 101), "bottom": (255, 183, 77),  "accent": (255, 255, 255)},
    {"name": "cool",   "top": (64, 144, 222),  "mid": (77, 182, 200),  "bottom": (129, 212, 250), "accent": (255, 255, 255)},
    {"name": "purple", "top": (126, 87, 194),  "mid": (149, 117, 205), "bottom": (186, 155, 211), "accent": (255, 255, 255)},
    {"name": "green",  "top": (67, 160, 71),   "mid": (102, 187, 106), "bottom": (165, 214, 167), "accent": (255, 255, 255)},
    {"name": "rose",   "top": (216, 67, 111),  "mid": (229, 115, 115), "bottom": (244, 143, 177), "accent": (255, 255, 255)},
]


def format_ass_time(seconds):
    """Convert seconds to ASS timecode H:MM:SS.cc"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def format_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_sentence(text, max_len=14):
    """Split a long sentence into subtitle-sized chunks on natural boundaries."""
    text = text.strip()
    if len(text) <= max_len:
        return [text]
    parts = []
    chunks = re.split(r'([，。！？；、,.\n])', text)
    buf = ""
    for ch in chunks:
        if len(buf) + len(ch) > max_len and buf:
            parts.append(buf)
            buf = ch if ch not in "，。！？；、,.\n" else ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf.strip())
    result = []
    for p in parts:
        while len(p) > max_len:
            result.append(p[:max_len])
            p = p[max_len:]
        if p.strip():
            result.append(p.strip())
    return result


def generate_ass(boundaries, ass_path, title, total_duration, hook_text=None):
    """Generate ASS subtitle file with intro hook + main subs + outro CTA."""

    # Build subtitle entries
    subs = []
    for sb in boundaries:
        start = sb["offset"]
        end = sb["offset"] + sb["duration"]
        text = sb["text"].strip()
        if not text:
            continue
        chunks = split_sentence(text, max_len=14)
        if len(chunks) == 1:
            subs.append({"start": start, "end": end, "text": chunks[0]})
        else:
            seg_dur = (end - start) / len(chunks)
            for i, ch in enumerate(chunks):
                subs.append({
                    "start": start + i * seg_dur,
                    "end": start + (i + 1) * seg_dur,
                    "text": ch
                })

    # ASS header
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Microsoft YaHei UI,64,&H00FFFFFF,&H00FFFFFF,&H66000000,&H99000000,-1,0,0,0,100,100,2,0,1,5,2,5,100,100,400,1
Style: Sub,Microsoft YaHei UI,46,&H00FFFFFF,&H00FFFFFF,&H66000000,&H99000000,-1,0,0,0,100,100,1,0,1,4,2,2,80,80,180,1
Style: Outro1,Microsoft YaHei UI,58,&H00FFFFFF,&H00FFFFFF,&H66000000,&H99000000,-1,0,0,0,100,100,0,0,1,5,2,5,100,100,350,1
Style: Outro2,Microsoft YaHei UI,36,&H00E0E0E0,&H00E0E0E0,&H66000000,&H99000000,0,0,0,0,100,100,0,0,1,3,1,5,100,100,270,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    lines = [header]

    # --- Intro hook (0 - 2.5s) ---
    hook = hook_text or title
    # Wrap hook to max 10 chars per line
    hook_lines = [hook[i:i+10] for i in range(0, len(hook), 10)][:3]
    hook_display = "\\N".join(hook_lines)
    lines.append(f"Dialogue: 0,0:00:00.00,0:00:02.50,Hook,,0,0,0,,{{\\fad(400,300)}}{hook_display}")

    # --- Main subtitles ---
    for s in subs:
        # Skip subs that overlap with intro/outro
        if s["start"] < 2.5:
            continue
        if s["end"] > total_duration - 3.5:
            continue
        lines.append(
            f"Dialogue: 0,{format_ass_time(s['start'])},{format_ass_time(s['end'])},Sub,,0,0,0,,"
            f"{{\\fad(150,150)}}{s['text']}"
        )

    # --- Outro CTA (last 3.5s) ---
    outro_start = max(total_duration - 3.5, 2.5)
    outro_end = total_duration + 0.5
    lines.append(
        f"Dialogue: 0,{format_ass_time(outro_start)},{format_ass_time(outro_end)},Outro1,,0,0,0,,"
        f"{{\\fad(400,300)}}关注@彩虹心理\\N每天懂一点心理学"
    )
    lines.append(
        f"Dialogue: 1,{format_ass_time(outro_start)},{format_ass_time(outro_end)},Outro2,,0,0,0,,"
        f"{{\\fad(400,300)}}觉得有用 点赞分享给需要的人"
    )

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return len(subs)


async def generate_tts(text, audio_path):
    """Generate TTS audio via edge-tts, return sentence boundary list."""
    comm = edge_tts.Communicate(text, voice=VOICE, rate=RATE)
    audio_data = b""
    boundaries = []

    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
        elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
            boundaries.append({
                "offset": chunk["offset"] / 10_000_000,
                "duration": chunk["duration"] / 10_000_000,
                "text": chunk["text"]
            })

    with open(audio_path, "wb") as f:
        f.write(audio_data)
    return boundaries


def create_background(theme, output_path):
    """Create enhanced 1080x1920 background with multi-layer gradient + decorations."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    top_c = theme["top"]
    mid_c = theme["mid"]
    bot_c = theme["bottom"]

    # 3-stop gradient: top -> mid -> bottom
    for y in range(HEIGHT):
        r = y / HEIGHT
        if r < 0.5:
            t = r * 2
            cr = int(top_c[0] + (mid_c[0] - top_c[0]) * t)
            cg = int(top_c[1] + (mid_c[1] - top_c[1]) * t)
            cb = int(top_c[2] + (mid_c[2] - top_c[2]) * t)
        else:
            t = (r - 0.5) * 2
            cr = int(mid_c[0] + (bot_c[0] - mid_c[0]) * t)
            cg = int(mid_c[1] + (bot_c[1] - mid_c[1]) * t)
            cb = int(mid_c[2] + (bot_c[2] - mid_c[2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(cr, cg, cb))

    img_rgba = img.convert("RGBA")

    # --- Decorative translucent circles (varied sizes/positions) ---
    circles = [
        (140, 250, 120, 22),
        (940, 380, 80, 18),
        (80, 700, 160, 15),
        (960, 1050, 200, 20),
        (200, 1300, 100, 12),
        (880, 1600, 140, 16),
        (540, 500, 250, 8),
    ]
    for cx, cy, rad, alpha in circles:
        layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 255, 255, alpha))
        img_rgba = Image.alpha_composite(img_rgba, layer)

    # --- Dot grid pattern (subtle texture) ---
    dot_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot_layer)
    for x in range(40, WIDTH, 60):
        for y in range(40, HEIGHT, 60):
            dd.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255, 10))
    img_rgba = Image.alpha_composite(img_rgba, dot_layer)

    # --- Content card (semi-transparent rounded rect in center) ---
    card_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card_layer)
    card_x1, card_y1 = 60, 380
    card_x2, card_y2 = WIDTH - 60, HEIGHT - 420
    cd.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=30, fill=(255, 255, 255, 20))
    # Card border
    cd.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=30, outline=(255, 255, 255, 40), width=2)
    img_rgba = Image.alpha_composite(img_rgba, card_layer)

    # --- Top brand bar ---
    brand_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bd = ImageDraw.Draw(brand_layer)
    bd.rounded_rectangle([0, 0, WIDTH, 130], radius=0, fill=(0, 0, 0, 50))
    img_rgba = Image.alpha_composite(img_rgba, brand_layer)

    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # --- Brand text (top center) ---
    try:
        f_brand = ImageFont.truetype(FONT_BOLD, 40)
        f_tag = ImageFont.truetype(FONT_REGULAR, 26)
    except Exception:
        f_brand = f_tag = ImageFont.load_default()

    brand = "\U0001f308 彩虹心理"
    bb = draw.textbbox((0, 0), brand, font=f_brand)
    draw.text(((WIDTH - (bb[2] - bb[0])) / 2, 45), brand, fill=(255, 255, 255), font=f_brand)

    # --- Bottom CTA bar ---
    cta_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cta_d = ImageDraw.Draw(cta_layer)
    cta_d.rounded_rectangle([0, HEIGHT - 180, WIDTH, HEIGHT], radius=0, fill=(0, 0, 0, 60))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, cta_layer)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    cta = "关注@彩虹心理  ·  每天懂一点心理学"
    cb = draw.textbbox((0, 0), cta, font=f_tag)
    draw.text(((WIDTH - (cb[2] - cb[0])) / 2, HEIGHT - 100), cta, fill=(255, 255, 255), font=f_tag)

    # --- Side accent line ---
    draw.line([(40, 200), (40, HEIGHT - 220)], fill=(255, 255, 255), width=3)
    draw.line([(WIDTH - 40, 200), (WIDTH - 40, HEIGHT - 220)], fill=(255, 255, 255), width=3)

    img.save(output_path, quality=95)
    return output_path


def get_audio_duration(audio_path):
    """Get audio duration in seconds via ffmpeg stderr parsing."""
    cmd = [FFMPEG, "-i", audio_path, "-f", "null", "-"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        for line in r.stderr.split("\n"):
            if "Duration" in line:
                ts = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = ts.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
    except Exception:
        pass
    return 0.0


def build_video(bg_path, audio_path, ass_path, output_path, duration, tmp_dir, bgm_path=None):
    """Combine background + audio + ASS subtitles into MP4."""
    # Use relative paths for filters
    ass_rel = "subs.ass"

    vf = f"subtitles={ass_rel}"

    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", bg_path,
        "-i", audio_path,
    ]

    # Add BGM if available
    if bgm_path and os.path.exists(bgm_path):
        cmd.extend(["-i", bgm_path])
        # Audio filter: mix TTS (full volume) + BGM (15% volume)
        cmd.extend([
            "-filter_complex",
            f"[0:v]{vf}[v];[1:a]volume=1.0[a1];[2:a]volume=0.15,afade=t=out:st={duration-2}:d=2[bgm];[a1][bgm]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "[v]", "-map", "[a]",
        ])
    else:
        cmd.extend(["-vf", vf])

    cmd.extend([
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-t", f"{duration + 0.5:.2f}",
        "-shortest",
        output_path
    ])

    r = subprocess.run(cmd, cwd=tmp_dir, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-800:] + "\n")
        return False
    return True


def extract_hook(content, title):
    """Extract the most impactful sentence from content as the hook."""
    sentences = re.split(r'[。！？\n]', content)
    # Find the shortest impactful sentence (usually the hook)
    for s in sentences:
        s = s.strip()
        if 8 <= len(s) <= 30:
            return s
    # Fallback: use title
    return title


async def make_video(title, content, output_path, theme_idx=0, bgm_path=None):
    """Main: create one short video from title + content."""
    theme = THEMES[theme_idx % len(THEMES)]
    output_path = os.path.abspath(output_path)
    base = os.path.dirname(output_path)
    tmp_dir = os.path.abspath(os.path.join(base, "_tmp_video_" + str(theme_idx)))
    os.makedirs(tmp_dir, exist_ok=True)

    audio_path = os.path.join(tmp_dir, "audio.mp3")
    ass_path = os.path.join(tmp_dir, "subs.ass")
    bg_path = os.path.join(tmp_dir, "background.png")

    # Extract hook from content
    hook = extract_hook(content, title)

    # Build TTS script: hook intro + content + outro CTA
    tts_script = f"{hook}。{content}。关注彩虹心理，每天懂一点心理学。觉得有用，点赞分享给需要的人。"

    print(f"[1/5] TTS: {title[:30]}...  hook={hook[:20]}...")
    boundaries = await generate_tts(tts_script, audio_path)
    print(f"  {len(boundaries)} sentence boundaries")

    print("[2/5] Duration...")
    dur = get_audio_duration(audio_path)
    if dur == 0:
        dur = len(tts_script) / 4.0
    print(f"  duration={dur:.1f}s")

    print("[3/5] ASS subtitles...")
    n = generate_ass(boundaries, ass_path, title, dur, hook_text=hook)
    print(f"  {n} subtitle segments")

    print("[4/5] Background...")
    create_background(theme, bg_path)

    print("[5/5] ffmpeg compose...")
    ok = build_video(bg_path, audio_path, ass_path, output_path, dur, tmp_dir, bgm_path)

    try:
        shutil.rmtree(tmp_dir)
    except Exception:
        pass

    if ok:
        sz = os.path.getsize(output_path) / 1024
        print(f"OK  {output_path}  ({sz:.0f} KB, {dur:.0f}s)")
    else:
        print(f"FAIL {output_path}")
    return ok


def main():
    ap = argparse.ArgumentParser(description="彩虹心理短视频生成器 v2.0")
    ap.add_argument("--title", required=True, help="文章标题")
    ap.add_argument("--content", required=True, help="文章内容(或.txt文件路径)")
    ap.add_argument("--output", required=True, help="输出MP4路径")
    ap.add_argument("--theme", type=int, default=0, help="配色索引 0-4")
    ap.add_argument("--bgm", default=None, help="背景音乐MP3路径(可选)")
    args = ap.parse_args()

    content = args.content
    if os.path.isfile(args.content):
        with open(args.content, "r", encoding="utf-8") as f:
            content = f.read()

    asyncio.run(make_video(args.title, content, args.output, args.theme, args.bgm))


if __name__ == "__main__":
    main()
