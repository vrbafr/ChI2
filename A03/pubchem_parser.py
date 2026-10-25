"""Print IUPAC names from a PubChem XML search export."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from bs4 import BeautifulSoup


def extract_iupac_names(xml_path: Path) -> list[str]:
    """Return all non-empty IUPAC names from a PubChem XML export."""
    with xml_path.open(encoding="utf-8") as xml_file:
        soup = BeautifulSoup(xml_file, "xml")

    return [
        name
        for tag in soup.find_all("iupacname")
        if (name := tag.get_text(strip=True))
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and print the exported compound IUPAC names."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "xml_file",
        type=Path,
        help="PubChem XML export to parse",
    )
    args = parser.parse_args(argv)

    for name in extract_iupac_names(args.xml_file):
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
