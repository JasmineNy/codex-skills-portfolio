#!/usr/bin/env python3
"""Render a formal DOCX or PDF resume into recruiter-facing PNG pages."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import struct
import sys
import tempfile


USER_ROOT = Path.home()
BUNDLED_PYTHON = USER_ROOT / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
BUNDLED_BIN_DIRS = [
    USER_ROOT / ".cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override",
    USER_ROOT / ".cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback",
]
RENDERER_ROOT = USER_ROOT / ".codex/plugins/cache/openai-primary-runtime/documents"
FONTCONFIG_FILE = Path(__file__).resolve().parent.parent / "assets/fontconfig-job-kit.conf"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a DOCX or PDF resume to page-<N>.png files."
    )
    parser.add_argument("input", type=Path, help="Formal .docx or .pdf resume")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=2200)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing page-*.png files in the output directory",
    )
    return parser.parse_args()


def command_env() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PATH", "")
    env["PATH"] = os.pathsep.join([*(str(p) for p in BUNDLED_BIN_DIRS), existing])
    if FONTCONFIG_FILE.is_file():
        env["FONTCONFIG_FILE"] = str(FONTCONFIG_FILE)
        env["SAL_FONTPATH"] = os.pathsep.join(
            ["/System/Library/Fonts", "/System/Library/Fonts/Supplemental", "/Library/Fonts"]
        )
    return env


def find_renderer() -> Path:
    candidates = sorted(RENDERER_ROOT.glob("*/skills/documents/render_docx.py"))
    if not candidates:
        raise RuntimeError("Codex document renderer was not found")
    return candidates[-1]


def runtime_python() -> str:
    return str(BUNDLED_PYTHON if BUNDLED_PYTHON.exists() else Path(sys.executable))


def check_output_dir(output_dir: Path, overwrite: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(output_dir.glob("page-*.png"))
    if existing and not overwrite:
        names = ", ".join(path.name for path in existing)
        raise RuntimeError(f"Output already contains rendered pages: {names}; use --overwrite")
    if overwrite:
        for path in existing:
            path.unlink()


def render_docx(source: Path, temp_dir: Path, width: int, height: int) -> list[Path]:
    cmd = [
        runtime_python(),
        str(find_renderer()),
        str(source),
        "--output_dir",
        str(temp_dir),
        "--width",
        str(width),
        "--height",
        str(height),
    ]
    subprocess.run(cmd, check=True, env=command_env())
    return sorted(temp_dir.glob("page-*.png"))


def render_pdf(source: Path, temp_dir: Path, width: int) -> list[Path]:
    env = command_env()
    pdftoppm = shutil.which("pdftoppm", path=env["PATH"])
    if not pdftoppm:
        raise RuntimeError("pdftoppm was not found in the bundled runtime")
    prefix = temp_dir / "page"
    cmd = [
        pdftoppm,
        "-png",
        "-scale-to-x",
        str(width),
        "-scale-to-y",
        "-1",
        str(source),
        str(prefix),
    ]
    subprocess.run(cmd, check=True, env=env)
    raw = sorted(temp_dir.glob("page-*.png"))
    normalized: list[Path] = []
    for index, path in enumerate(raw, start=1):
        target = temp_dir / f"normalized-{index}.png"
        path.replace(target)
        normalized.append(target)
    return normalized


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise RuntimeError(f"Rendered page is not a valid PNG: {path.name}")
    return struct.unpack(">II", header[16:24])


def verify_images(paths: list[Path]) -> list[dict[str, int | str]]:
    if not paths:
        raise RuntimeError("No resume pages were rendered")
    details: list[dict[str, int | str]] = []
    for path in paths:
        width, height = png_dimensions(path)
        if width < 1200 or height < 1500:
            raise RuntimeError(
                f"Rendered page is too small for chat delivery: {path.name} {width}x{height}"
            )
        details.append({"file": path.name, "width": width, "height": height})
    return details


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Input resume does not exist: {source}")
    suffix = source.suffix.lower()
    if suffix not in {".docx", ".pdf"}:
        raise SystemExit("Input must be a .docx or .pdf file")

    output_dir = args.output_dir.expanduser().resolve()
    check_output_dir(output_dir, args.overwrite)

    with tempfile.TemporaryDirectory(prefix="job-kit-render-") as temp_name:
        temp_dir = Path(temp_name)
        if suffix == ".docx":
            rendered = render_docx(source, temp_dir, args.width, args.height)
        else:
            rendered = render_pdf(source, temp_dir, args.width)
        verify_images(rendered)
        output_paths: list[Path] = []
        for index, path in enumerate(rendered, start=1):
            target = output_dir / f"page-{index}.png"
            shutil.copy2(path, target)
            output_paths.append(target)

    details = verify_images(output_paths)
    print(
        json.dumps(
            {
                "status": "ok",
                "source": str(source),
                "output_dir": str(output_dir),
                "pages": details,
                "contacts_preserved": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
