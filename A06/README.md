# A06 — Plot a linear relationship

`graph.csv` contains 21 points for assignment 1, the linear relationship
`y = 2x`. The script reads the CSV and generates `graph.png` in this directory.

## Clone the repository

```powershell
git clone https://github.com/vrbafr/ChI2.git
cd ChI2
```

## Set up the environment

Create and activate a virtual environment from the repository root, then
install the plotting dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r A06\requirements.txt
```

## Generate the graph

Run this from the repository root:

```powershell
python A06\graph.py
```

The script writes `A06\graph.png`. Run it again whenever `graph.csv` changes.
