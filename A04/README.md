# A04 — SQLite database from CSV files

`db.py` imports the CSV files named on the command line into `db.sqlite` in the
current working directory. Each table is named after its CSV file (without the
extension), and its columns are read from the first CSV row. Tables that
already exist are left unchanged. After importing, the script prints the total
population of countries where English is an official language.

The script uses only the Python standard library (`csv` and `sqlite3`), so
`requirements.txt` contains no third-party dependencies.

## Run from the repository root

Download `world.zip` from the course Moodle resource
<https://dl2.cuni.cz/mod/resource/view.php?id=20491> (a Moodle login may be
required), then extract it:

```powershell
python -m pip install -r A04\requirements.txt
Expand-Archive -Path A04\world.zip -DestinationPath A04\world
python A04\db.py A04\world\city.csv A04\world\country.csv A04\world\countrylanguage.csv
```

The archive uses semicolon-delimited CSV files; the script detects the
delimiter. The import command creates `db.sqlite` in the current directory.
It only needs to be run once for each table. To query the existing database
without re-importing any files, run:

```powershell
python A04\db.py
```

The output contains the question and its computed answer. For the standard
`world` dataset, the answer is the sum of `country.Population` for each country
whose `countrylanguage` row has `Language = 'English'` and `IsOfficial = 'T'`.
With the included archive, the total is **459158800**.
