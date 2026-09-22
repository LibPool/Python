#!/usr/bin/env python3
"""Generate the LibPool Python library index from PyPI metadata.

Layout:
  python-v3/<package-name>/<package-name>.md

Run from the repo root:
    python tools/generate_index.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


PYPI = "https://pypi.org/pypi"
USER_AGENT = "LibPool-Indexer/1.0 (+https://github.com/LibPool)"
CACHE_PATH = Path(__file__).resolve().parent / "cache" / "pypi.json"
OUT_DIR = "python-v3"


@dataclass
class PyLib:
    name: str
    tags: list[str] = field(default_factory=list)
    version: str = ""
    summary: str = ""
    homepage: str = ""
    repository: str = ""
    requires_python: str = ""
    license: str = ""
    classifiers: list[str] = field(default_factory=list)
    versions: list[str] = field(default_factory=list)

    @property
    def safe_name(self) -> str:
        return re.sub(r"[^A-Za-z0-9._+-]", "-", self.name)


def http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def load_seeds(path: Path) -> list[PyLib]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [PyLib(name=item["name"], tags=item.get("tags", [])) for item in data]


def load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def enrich(lib: PyLib, cache: dict, use_cache: bool) -> None:
    key = lib.name
    if use_cache and key in cache:
        entry = cache[key]
        for attr in ("version", "summary", "homepage", "repository", "requires_python", "license", "classifiers", "versions"):
            setattr(lib, attr, entry.get(attr, ""))
        lib.tags = list(dict.fromkeys(lib.tags + entry.get("tags", [])))
        return

    try:
        data = http_json(f"{PYPI}/{urllib.parse.quote(lib.name)}/json")
    except Exception as exc:
        print(f"  {lib.name}: fetch failed -> {exc}", flush=True)
        return
    info = data.get("info") or {}
    lib.name = info.get("name") or lib.name
    lib.version = info.get("version") or ""
    lib.summary = (info.get("summary") or "").strip()
    lib.requires_python = (info.get("requires_python") or "").strip()
    lib.license = (info.get("license") or "").strip()
    lib.classifiers = info.get("classifiers") or []
    lib.versions = sorted(data.get("releases", {}).keys())
    urls = info.get("project_urls") or {}
    lib.homepage = (info.get("home_page") or urls.get("Homepage") or urls.get("Home") or "").strip()
    lib.repository = (urls.get("Source") or urls.get("Repository") or urls.get("Code") or "").strip()
    if not lib.homepage:
        lib.homepage = f"https://pypi.org/project/{urllib.parse.quote(lib.name)}/"
    cache[key] = {
        "name": lib.name,
        "version": lib.version,
        "summary": lib.summary,
        "homepage": lib.homepage,
        "repository": lib.repository,
        "requires_python": lib.requires_python,
        "license": lib.license,
        "classifiers": lib.classifiers,
        "versions": lib.versions,
        "tags": lib.tags,
    }


def readme_md(lib: PyLib) -> str:
    version_lines = "\n".join(f"- {v}" for v in lib.versions[-12:] or ["-"])
    if len(lib.versions) > 12:
        version_lines += f"\n- 共 {len(lib.versions)} 个版本，完整清单见 PyPI。"
    websites = []
    if lib.homepage:
        websites.append(f"- 官网：{lib.homepage}")
    if lib.repository and lib.repository != lib.homepage:
        websites.append(f"- 源码仓库：{lib.repository}")
    websites.append(f"- PyPI 项目页：https://pypi.org/project/{urllib.parse.quote(lib.name)}/")
    downloads = [
        f"- pip 安装：`pip install {lib.name}`",
        f"- 下载页面：https://pypi.org/project/{urllib.parse.quote(lib.name)}/#files",
    ]
    if lib.requires_python:
        downloads.append(f"- 运行要求：Python {lib.requires_python}")

    tags = ", ".join(sorted(set(lib.tags))) if lib.tags else "Python"
    desc = lib.summary or f"{lib.name} - Python library from PyPI"
    return f"""# {lib.name}

> 标签: {tags}

## 简介

{desc}

## 官网

{chr(10).join(websites)}

## 历史版本号

- 当前版本：{lib.version or "未知"}

{version_lines}

## 获取地址

{chr(10).join(downloads)}
"""


def generate(root: Path, libs: list[PyLib], out_dir: Path) -> dict[str, int]:
    counts = defaultdict(int)
    for lib in libs:
        if not lib.version:
            continue
        text = readme_md(lib)
        target = out_dir / lib.safe_name
        target.mkdir(parents=True, exist_ok=True)
        (target / f"{lib.safe_name}.md").write_text(text, encoding="utf-8")
        counts[lib.safe_name] += 1
    return dict(counts)


def write_python_readme(root: Path, libs: list[PyLib]) -> None:
    lines = [
        "# Python 库索引",
        "",
        "本目录收录来自 PyPI 的 Python 库索引，按发行包名路径组织：",
        "",
        "- 版本目录：`python-v3`（当前种子以 Python 3 生态为主）",
        f"- 包路径：`{OUT_DIR}/<包名>/<包名>.md`",
        f"- 当前共收录 {len(libs)} 个 PyPI 项目，覆盖 Web、数据科学、AI、云原生、测试、安全等常见领域。",
        "",
        "## 数据源",
        "",
        "- PyPI JSON API：https://pypi.org/pypi/<package>/json",
        "- PyPI 官网：https://pypi.org/",
        "",
        "## 生成方式",
        "",
        "```bash",
        "python tools/build_seed_list.py",
        "python tools/generate_index.py",
        "```",
        "",
    ]
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="tools/seeds/python.json")
    ap.add_argument("--out", default=".")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--refresh-cache", action="store_true")
    args = ap.parse_args()

    root = Path(args.out).resolve()
    libs = load_seeds(Path(args.seeds))
    if args.limit:
        libs = libs[: args.limit]
    cache = load_cache()
    print(f"Processing {len(libs)} packages from {args.seeds}...", flush=True)
    for i, lib in enumerate(libs, 1):
        enrich(lib, cache, use_cache=not args.refresh_cache)
        print(f"  [{i}/{len(libs)}] {lib.name} -> {lib.version or 'failed'}", flush=True)
        time.sleep(0.05)
    save_cache(cache)
    counts = generate(root, libs, root)
    print("Generated:", json.dumps(counts, sort_keys=True), flush=True)
    write_python_readme(root, libs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
