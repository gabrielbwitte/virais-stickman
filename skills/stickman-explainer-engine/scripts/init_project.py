#!/usr/bin/env python3
"""Initialize a stickman video project without overwriting existing work."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Optional


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_duration(minutes_text: str) -> tuple[Decimal, Decimal]:
    try:
        minutes = Decimal(minutes_text)
    except InvalidOperation as exc:
        raise ValueError("duration must be a positive number of minutes") from exc
    if not minutes.is_finite() or minutes <= 0:
        raise ValueError("duration must be a positive finite number of minutes")

    return minutes, minutes * Decimal(60)


def decimal_text(value: Decimal) -> str:
    normalized = value.normalize()
    return format(normalized, "f")


def initialize(output_dir: Path, slug: str, minutes_text: str, aspect_ratio: Optional[str] = None) -> dict:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug must use lowercase letters, digits, and single hyphens")

    minutes, total_seconds = parse_duration(minutes_text)
    project_dir = output_dir.expanduser().resolve() / f"stickman-{slug}"
    scenes_dir = project_dir / "cenas"
    manifest_path = project_dir / "manifesto_producao.json"
    map_path = project_dir / "mapa_cenas.json"

    project_dir.mkdir(parents=True, exist_ok=True)
    scenes_dir.mkdir(parents=True, exist_ok=True)

    if manifest_path.exists() or map_path.exists():
        if not manifest_path.exists() or not map_path.exists():
            raise FileExistsError(
                f"partial project metadata exists in {project_dir}; refusing to overwrite"
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema_version") != 2:
            raise FileExistsError(
                f"project {project_dir} uses an older manifest schema; refusing to reinterpret or overwrite it"
            )
        if (
            manifest.get("slug") != slug
            or manifest.get("duration_seconds") != decimal_text(total_seconds)
            or (aspect_ratio is not None and manifest.get("aspect_ratio") != aspect_ratio)
        ):
            raise FileExistsError(
                f"project {project_dir} already exists with different metadata; refusing to overwrite"
            )
        return {
            "status": "resumed",
            "project_dir": str(project_dir),
            "scene_count": manifest.get("scene_count"),
            "duration_seconds": manifest.get("duration_seconds"),
        }

    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        "schema_version": 2,
        "slug": slug,
        "status": "initialized",
        "created_at": now,
        "duration_minutes": decimal_text(minutes),
        "duration_seconds": decimal_text(total_seconds),
        "actual_audio_duration_seconds": None,
        "scene_count": None,
        "aspect_ratio": aspect_ratio,
        "palette": None,
        "saturation": None,
        "style_anchor_file": "style_anchor.txt",
        "script_status": "pending",
        "cast_status": "pending",
        "visual_brief_status": "pending",
        "approvals": {},
        "models": {},
        "files": {},
        "delivery": {},
    }
    scene_map = {
        "schema_version": 2,
        "slug": slug,
        "duration_seconds": decimal_text(total_seconds),
        "actual_audio_duration_seconds": None,
        "scene_count": None,
        "timeline_status": "pending",
        "scenes": [],
    }

    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    map_path.write_text(json.dumps(scene_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "created",
        "project_dir": str(project_dir),
        "scene_count": None,
        "duration_seconds": decimal_text(total_seconds),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--duration-minutes", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--aspect-ratio")
    args = parser.parse_args()
    try:
        result = initialize(Path(args.output_dir), args.slug, args.duration_minutes, args.aspect_ratio)
    except (ValueError, FileExistsError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
