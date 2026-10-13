"""Build one WebUI import file; no production files or database changes."""

from pathlib import Path
import sys


def build():
    root = Path(__file__).resolve().parent
    header = '''"""
title: Administrative Bounded Synthetic Test
description: Isolated synthetic project reads; no accounts or external actions.
version: 0.3.0
"""
'''
    return header + (root / "admin_bounded_controller.py").read_text(encoding="utf-8") + "\n" + (root / "admin_webui_pipe.py").read_text(encoding="utf-8")


if __name__ == "__main__":
    target = Path(sys.argv[1])
    target.write_text(build(), encoding="utf-8")
    print("Synthetic Pipe bundle written")
