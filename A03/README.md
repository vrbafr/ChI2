# A04 — PubChem benzidine compounds

`pubchem_benzidine.xml` contains the XML export of the 226 compound results
from a PubChem search for `benzidine`. The export was obtained through the
search-results **Download → XML** option on
[PubChem](https://pubchem.ncbi.nlm.nih.gov/).

The script uses BeautifulSoup's XML parser to print each non-empty IUPAC name,
one per line.

From the repository root, install the dependencies and pass the XML file as
the first command-line argument:

```console
python -m pip install -r A04/requirements.txt
python A04/pubchem_parser.py A04/pubchem_benzidine.xml
```
