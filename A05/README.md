# A05 — Convert ChemDraw CDXML files to SDF

`cdxml2sdf.py` converts one or more ChemDraw `.cdxml` files into a single
`.sdf` file. RDKit reads CDXML, which the installed Open Babel build does not
support as an input format; Open Babel then writes the SDF and compares the
molecules with FP2 fingerprints to find the highest Tanimoto similarity. RDKit
sanitization is disabled during parsing so structures with ChemDraw valence
warnings, such as the included aluminum compound, are preserved for Open Babel.

## Clone the repository

```powershell
git clone https://github.com/vrbafr/ChI2.git
cd ChI2
```

## Set up the environment

From the repository root, create and activate a virtual environment, then
install the required packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r A05\requirements.txt
```

## Add CDXML files and run

Download the course [CDXML archive](https://dl2.cuni.cz/mod/resource/view.php?id=112386)
(a Moodle login may be required), then extract its `.cdxml` files into the
`A05` directory. From that directory, pass a quoted wildcard pattern so the
script can expand it on Windows:

```powershell
cd A05
python cdxml2sdf.py "*.cdxml"
```

The script writes (and overwrites) `cdxml2sdf.sdf` by default. To choose a
different output path, include a `.sdf` argument whose file does not already
exist:

```powershell
python cdxml2sdf.py "*.cdxml" "converted.sdf"
```

If the named SDF file already exists, the default `cdxml2sdf.sdf` output is
used and overwritten. The script prints the most similar pair of molecules
and their Tanimoto value to standard output.
