#!/usr/bin/env python3
"""Convert ChemDraw CDXML files to one SDF file and find the closest pair."""

from __future__ import annotations

import argparse
import glob
import itertools
import sys
from pathlib import Path

try:
    from openbabel import pybel
except ImportError as error:
    raise SystemExit(
        "Open Babel's Python bindings are required. Install them with "
        "'python -m pip install -r requirements.txt'."
    ) from error

try:
    from rdkit import Chem
except ImportError as error:
    raise SystemExit(
        "RDKit is required to read CDXML files. Install dependencies with "
        "'python -m pip install -r requirements.txt'."
    ) from error


def expand_inputs(arguments: list[str]) -> tuple[Path, list[Path]]:
    output_path = Path("cdxml2sdf.sdf")
    input_patterns: list[str] = []

    for argument in arguments:
        candidate = Path(argument)
        if candidate.suffix.lower() == ".sdf":
            if not candidate.exists():
                output_path = candidate
        else:
            input_patterns.append(argument)

    inputs = sorted(
        {
            Path(match)
            for pattern in input_patterns
            for match in glob.glob(pattern)
            if Path(match).is_file() and Path(match).suffix.lower() == ".cdxml"
        },
        key=lambda path: str(path).lower(),
    )
    return output_path, inputs


def convert_files(
    inputs: list[Path],
) -> list[tuple[str, pybel.Molecule, pybel.Fingerprint]]:
    converted: list[tuple[str, pybel.Molecule, pybel.Fingerprint]] = []

    for path in inputs:
        rdkit_molecules = Chem.MolsFromCDXMLFile(str(path), sanitize=False)
        if not rdkit_molecules:
            raise ValueError(f"No molecule could be read from {path}")
        for rdkit_molecule in rdkit_molecules:
            mol_block = Chem.MolToMolBlock(rdkit_molecule)
            molecule = pybel.readstring("mol", mol_block)
            molecule.title = path.name
            converted.append((path.name, molecule, molecule.calcfp("FP2")))

    return converted


def write_sdf(
    output_path: Path,
    molecules: list[tuple[str, pybel.Molecule, pybel.Fingerprint]],
) -> None:
    output = pybel.Outputfile("sdf", str(output_path), overwrite=True)
    try:
        for _, molecule, _ in molecules:
            output.write(molecule)
    finally:
        output.close()


def closest_pair(
    molecules: list[tuple[str, pybel.Molecule, pybel.Fingerprint]],
) -> tuple[str, str, float]:
    best_pair: tuple[str, str, float] | None = None
    for first, second in itertools.combinations(molecules, 2):
        similarity = first[2] | second[2]
        if best_pair is None or similarity > best_pair[2]:
            best_pair = (first[0], second[0], similarity)

    if best_pair is None:
        raise ValueError("At least two molecules are required to compare similarity.")
    return best_pair


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert CDXML files to a single SDF and report the closest pair."
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="CDXML file names or wildcard patterns; an optional new .sdf path selects output",
    )
    arguments = parser.parse_args()

    output_path, inputs = expand_inputs(arguments.files)
    if not inputs:
        parser.error("no matching .cdxml input files were found")

    molecules = convert_files(inputs)
    first, second, similarity = closest_pair(molecules)
    write_sdf(output_path, molecules)
    print(
        f"Most similar molecules: {first} and {second} "
        f"(Tanimoto: {similarity:.4f})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
