#!/usr/bin/env python3
"""Render a variable-duration scene timeline and narration into a local MP4."""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Optional


ALLOWED_TRANSITIONS = {
    "cut",
    "fade",
    "fadeblack",
    "fadewhite",
    "dissolve",
    "wipeleft",
    "wiperight",
    "slideleft",
    "slideright",
    "zoomin",
}


class RenderError(RuntimeError):
    pass


def run(command: list[str]) -> subprocess.CompletedProcess:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip()[-2500:]
        raise RenderError(f"command failed ({result.returncode}): {detail}")
    return result


def inside_project(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"path must stay inside project directory: {relative_path}") from exc
    if not candidate.is_file():
        raise FileNotFoundError(f"required project file not found: {candidate}")
    return candidate


def probe(path: Path, ffprobe: str) -> dict[str, Any]:
    result = run([
        ffprobe,
        "-v", "error",
        "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
        "-of", "json",
        str(path),
    ])
    data = json.loads(result.stdout)
    duration = Decimal(str(data.get("format", {}).get("duration", "0")))
    if not duration.is_finite() or duration <= 0:
        raise RenderError(f"could not read a positive media duration: {path}")
    return {"duration": duration, "streams": data.get("streams", [])}


def positive_decimal(value: Any, label: str) -> Decimal:
    try:
        parsed = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{label} must be a number") from exc
    if not parsed.is_finite() or parsed <= 0:
        raise ValueError(f"{label} must be a positive finite number")
    return parsed


def even(value: float) -> int:
    rounded = max(2, int(round(value)))
    return rounded if rounded % 2 == 0 else rounded + 1


def output_size(aspect_ratio: str, override: Optional[list[int]]) -> tuple[int, int]:
    if override:
        width, height = override
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        return even(width), even(height)
    try:
        left, right = aspect_ratio.split(":", 1)
        ratio = float(Decimal(left) / Decimal(right))
    except (ValueError, InvalidOperation, ZeroDivisionError) as exc:
        raise ValueError("aspect_ratio must use a ratio such as 16:9 or 9:16") from exc
    if ratio <= 0 or not math.isfinite(ratio):
        raise ValueError("aspect_ratio must be positive")
    if math.isclose(ratio, 1.0, rel_tol=0.0, abs_tol=1e-6):
        return 1080, 1080
    if ratio > 1:
        return 1920, even(1920 / ratio)
    return even(1920 * ratio), 1920


def transition_for(scene: dict[str, Any]) -> tuple[str, Decimal]:
    raw = scene.get("transition_out", {"type": "cut", "duration_seconds": 0})
    if isinstance(raw, str):
        transition_type = raw.lower()
        raw_duration = 0 if transition_type == "cut" else 0.4
    elif isinstance(raw, dict):
        transition_type = str(raw.get("type", "cut")).lower()
        raw_duration = raw.get("duration_seconds", 0)
    else:
        raise ValueError("transition_out must be a string or object")
    if transition_type not in ALLOWED_TRANSITIONS:
        raise ValueError(f"unsupported transition type: {transition_type}")
    if transition_type == "cut":
        return "cut", Decimal(0)
    duration = positive_decimal(raw_duration, "transition duration")
    return transition_type, duration


def normalize_scene(
    source: Path,
    target: Path,
    clip_duration: Decimal,
    width: int,
    height: int,
    fps: int,
    ffmpeg: str,
    ffprobe: str,
) -> None:
    is_image = source.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    vf_tail = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"setsar=1,fps={fps},format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS"
    )
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    if is_image:
        command += ["-loop", "1", "-framerate", str(fps), "-i", str(source)]
        vf = vf_tail
    else:
        source_duration = probe(source, ffprobe)["duration"]
        pad_seconds = max(Decimal(0), clip_duration - source_duration)
        vf = (
            f"trim=duration={float(clip_duration):.6f},setpts=PTS-STARTPTS,"
            f"tpad=stop_mode=clone:stop_duration={float(pad_seconds):.6f},"
            f"{vf_tail}"
        )
        command += ["-i", str(source)]
    command += [
        "-vf", vf,
        "-an",
        "-t", f"{float(clip_duration):.6f}",
        "-r", str(fps),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(target),
    ]
    run(command)


def render(project_dir: Path, timeline_path: Path, audio_path: Path, output_path: Path,
           overwrite: bool = False) -> dict[str, Any]:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RenderError("both ffmpeg and ffprobe must be installed and available on PATH")
    root = project_dir.expanduser().resolve()
    timeline_file = inside_project(root, str(timeline_path))
    audio_file = inside_project(root, str(audio_path))
    timeline = json.loads(timeline_file.read_text(encoding="utf-8"))
    scenes = timeline.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("timeline.json must contain a non-empty scenes array")
    aspect_ratio = str(timeline.get("aspect_ratio", "16:9"))
    fps = int(timeline.get("fps", 30))
    if fps <= 0 or fps > 120:
        raise ValueError("fps must be between 1 and 120")
    override_size = timeline.get("resolution")
    if override_size is not None:
        if not isinstance(override_size, list) or len(override_size) != 2:
            raise ValueError("resolution must be [width, height]")
        override_size = [int(value) for value in override_size]
    width, height = output_size(aspect_ratio, override_size)
    expected_ratio = float(Decimal(aspect_ratio.split(":", 1)[0]) / Decimal(aspect_ratio.split(":", 1)[1]))
    actual_ratio = width / height
    if abs(actual_ratio - expected_ratio) > 0.002:
        raise ValueError("render resolution does not match the selected aspect ratio")

    audio_duration = probe(audio_file, ffprobe)["duration"]
    planned: list[dict[str, Any]] = []
    planned_total = Decimal(0)
    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise ValueError(f"scene {index} must be an object")
        duration = positive_decimal(scene.get("duration_seconds"), f"scene {index} duration")
        image = scene.get("image")
        video = scene.get("video")
        source = None
        source_kind = None
        if video:
            candidate = (root / str(video)).resolve()
            if candidate.is_file():
                source, source_kind = candidate, "video"
        if source is None and image:
            candidate = (root / str(image)).resolve()
            if candidate.is_file():
                source, source_kind = candidate, "image"
        if source is None:
            raise FileNotFoundError(f"scene {index} has neither an existing video nor image source")
        try:
            source.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"scene {index} media path must stay inside project directory") from exc
        transition_type, transition_duration = transition_for(scene)
        planned.append({
            "number": int(scene.get("number", index)),
            "source": source,
            "source_kind": source_kind,
            "planned_duration": duration,
            "transition_type": transition_type,
            "planned_transition_duration": transition_duration,
        })
        planned_total += duration

    if planned_total <= 0:
        raise ValueError("total planned scene duration must be positive")
    scale_factor = audio_duration / planned_total
    for item in planned:
        item["duration"] = item["planned_duration"] * scale_factor

    transition_records = []
    for index, item in enumerate(planned):
        if index == len(planned) - 1 or item["transition_type"] == "cut":
            item["transition_duration"] = Decimal(0)
        else:
            limit = min(item["duration"], planned[index + 1]["duration"]) * Decimal("0.45")
            item["transition_duration"] = min(item["planned_transition_duration"], limit)
        transition_records.append({
            "after_scene": item["number"],
            "type": item["transition_type"] if item["transition_duration"] > 0 else "cut",
            "duration_seconds": float(item["transition_duration"]),
        })

    output_path = output_path.expanduser()
    if not output_path.is_absolute():
        output_path = root / output_path
    output_path = output_path.resolve()
    try:
        output_path.relative_to(root)
    except ValueError as exc:
        raise ValueError("output must be inside the project directory") from exc
    if output_path.suffix.lower() != ".mp4":
        raise ValueError("output file must use the .mp4 extension")
    protected_inputs = {timeline_file, audio_file, *(item["source"] for item in planned)}
    if output_path in protected_inputs:
        raise ValueError("output path cannot replace the timeline, narration, or a scene source")
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"output already exists; choose a new name or pass --overwrite: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="stickman-render-", dir=str(root)) as temp_name:
        temp_dir = Path(temp_name)
        segment_paths: list[Path] = []
        for index, item in enumerate(planned):
            source_duration = item["duration"] + item["transition_duration"]
            segment = temp_dir / f"segment_{index:04d}.mp4"
            normalize_scene(
                item["source"], segment, source_duration, width, height, fps, ffmpeg, ffprobe
            )
            segment_paths.append(segment)

        inputs: list[str] = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
        for segment in segment_paths:
            inputs += ["-i", str(segment)]
        audio_index = len(segment_paths)
        inputs += ["-i", str(audio_file)]

        graph_parts = [f"[{index}:v]settb=AVTB,setpts=PTS-STARTPTS[s{index}]" for index in range(len(segment_paths))]
        current_label = "s0"
        current_duration = planned[0]["duration"] + planned[0]["transition_duration"]
        for index in range(1, len(segment_paths)):
            transition = planned[index - 1]["transition_duration"]
            next_label = f"v{index}"
            if transition > 0:
                offset = current_duration - transition
                graph_parts.append(
                    f"[{current_label}][s{index}]xfade="
                    f"transition={planned[index - 1]['transition_type']}:"
                    f"duration={float(transition):.6f}:offset={float(offset):.6f},"
                    f"format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[{next_label}]"
                )
                current_duration += planned[index]["duration"] + planned[index]["transition_duration"] - transition
            else:
                graph_parts.append(
                    f"[{current_label}][s{index}]concat=n=2:v=1:a=0,"
                    f"format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[{next_label}]"
                )
                current_duration += planned[index]["duration"] + planned[index]["transition_duration"]
            current_label = next_label

        target_seconds = float(audio_duration)
        graph_parts.append(
            f"[{audio_index}:a]aresample=48000,apad,"
            f"atrim=duration={target_seconds:.6f},asetpts=PTS-STARTPTS[aout]"
        )
        graph = ";".join(graph_parts)
        temp_output = temp_dir / "rendered.mp4"
        command = inputs + [
            "-filter_complex", graph,
            "-map", f"[{current_label}]",
            "-map", "[aout]",
            "-t", f"{target_seconds:.6f}",
            "-r", str(fps),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            str(temp_output),
        ]
        run(command)
        output_info = probe(temp_output, ffprobe)
        tolerance = max(Decimal(1) / Decimal(fps), Decimal("0.08"))
        if abs(output_info["duration"] - audio_duration) > tolerance:
            raise RenderError(
                f"rendered duration {output_info['duration']}s differs from narration "
                f"{audio_duration}s by more than {tolerance}s"
            )
        if output_path.exists() and not overwrite:
            raise FileExistsError(f"output appeared during render; refusing to overwrite: {output_path}")
        os.replace(temp_output, output_path)

    report = {
        "status": "rendered",
        "output": str(output_path),
        "audio_duration_seconds": float(audio_duration),
        "rendered_duration_seconds": float(output_info["duration"]),
        "duration_scale_factor": float(scale_factor),
        "aspect_ratio": aspect_ratio,
        "resolution": [width, height],
        "fps": fps,
        "scene_count": len(planned),
        "transitions": transition_records,
        "scenes": [
            {
                "number": item["number"],
                "source": str(item["source"].relative_to(root)),
                "source_kind": item["source_kind"],
                "duration_seconds": float(item["duration"]),
            }
            for item in planned
        ],
    }
    (root / "render_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True, type=Path)
    parser.add_argument("--timeline", default="timeline.json")
    parser.add_argument("--audio", default="narracao.mp3")
    parser.add_argument("--output", default="video_final.mp4", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        report = render(args.project_dir, Path(args.timeline), Path(args.audio), args.output, args.overwrite)
    except (ValueError, FileNotFoundError, FileExistsError, json.JSONDecodeError, OSError, RenderError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
