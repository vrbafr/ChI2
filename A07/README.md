# A07 — Five alanine molecules on a regular pentagon

`alanine.smi` describes L-alanine in SMILES. Open Babel generates its 3D
coordinates in `alanine.pov`; `ala5.pov` includes that molecule and places five
centered copies at the vertices of a regular pentagon. `babel_povray3.inc` is
the Open Babel include file required by the generated POV-Ray scene. The
rendered image is `ala5.png`.

## Clone the repository

```powershell
git clone https://github.com/vrbafr/ChI2.git
cd ChI2
```

## Install the tools

Create and activate a Python virtual environment, then install the Open Babel
wheel. The wheel includes the `obabel.exe` command and Open Babel data files:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install openbabel-wheel
```

Install POV-Ray for Windows:

```powershell
winget install --id PersistenceOfVisionRaytracer.POVRay --exact
```

## Generate the scene and render the image

Run these commands from the repository root in PowerShell. Open Babel writes
a standalone scene by default; `alanine.pov` is adapted for inclusion by
removing the generated camera, light, background, and final standalone
`mol_0` instance.

```powershell
$babel = ".\.venv\Lib\site-packages\openbabel\bin\obabel.exe"
$env:BABEL_DATADIR = ".\.venv\Lib\site-packages\openbabel\bin\data"
& $babel A07\alanine.smi -O A07\alanine.pov --gen3D
```

The checked-in `alanine.pov` already contains the converted 3D molecule with
those standalone scene elements removed. To render the checked-in scene with
POV-Ray 3.7, run:

```powershell
$povray = "$env:ProgramFiles\POV-Ray\v3.7\bin\pvengine64.exe"
& $povray /RENDER A07\ala5.pov /EXIT +W1200 +H900 +FN
```

POV-Ray writes `A07\ala5.png`.
