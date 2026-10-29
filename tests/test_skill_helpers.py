"""Local smoke tests for the skill's project and render helpers."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "stickman-explainer-engine" / "scripts"


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load helper script: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


init_project = load_script("init_project", SCRIPTS / "init_project.py")
render_video = load_script("render_video", SCRIPTS / "render_video.py")


class InitProjectTests(unittest.TestCase):
    def test_initializes_variable_timeline_without_fixed_scene_count(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = init_project.initialize(Path(temp_dir), "sample-video", "1.5", "16:9")
            self.assertEqual(result["duration_seconds"], "90")
            self.assertIsNone(result["scene_count"])

            project = Path(result["project_dir"])
            manifest = json.loads((project / "manifesto_producao.json").read_text())
            timeline = json.loads((project / "mapa_cenas.json").read_text())
            self.assertEqual(manifest["schema_version"], 2)
            self.assertIsNone(manifest["palette"])
            self.assertIsNone(manifest["saturation"])
            self.assertEqual(timeline["scenes"], [])

    def test_resumes_only_matching_project_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            init_project.initialize(root, "sample-video", "1", "16:9")
            result = init_project.initialize(root, "sample-video", "1", "16:9")
            self.assertEqual(result["status"], "resumed")
            with self.assertRaises(FileExistsError):
                init_project.initialize(root, "sample-video", "1", "9:16")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg is not installed")
class RenderVideoTests(unittest.TestCase):
    def test_renders_variable_stills_with_transition_and_narration(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                 "color=c=red:s=160x90:d=1", "-frames:v", "1", str(project / "scene1.png")],
                check=True,
            )
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                 "color=c=blue:s=160x90:d=1", "-frames:v", "1", str(project / "scene2.png")],
                check=True,
            )
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                 "sine=frequency=440:duration=1.4", "-c:a", "pcm_s16le", str(project / "narracao.wav")],
                check=True,
            )
            timeline = {
                "aspect_ratio": "16:9",
                "resolution": [320, 180],
                "fps": 24,
                "scenes": [
                    {"number": 1, "image": "scene1.png", "duration_seconds": 0.55,
                     "transition_out": {"type": "fade", "duration_seconds": 0.2}},
                    {"number": 2, "image": "scene2.png", "duration_seconds": 0.85,
                     "transition_out": {"type": "cut", "duration_seconds": 0}},
                ],
            }
            (project / "timeline.json").write_text(json.dumps(timeline), encoding="utf-8")

            report = render_video.render(
                project, Path("timeline.json"), Path("narracao.wav"), Path("video_final.mp4")
            )
            self.assertTrue(Path(report["output"]).is_file())
            self.assertEqual(report["resolution"], [320, 180])
            self.assertEqual(report["transitions"][0]["type"], "fade")
            self.assertLess(abs(report["rendered_duration_seconds"] - 1.4), 0.08)


if __name__ == "__main__":
    unittest.main()
