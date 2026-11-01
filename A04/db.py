"""Load CSV files into SQLite and report the population of English-speaking countries."""

import csv
import sqlite3
import sys
from collections.abc import Sequence
from pathlib import Path


class WorldDatabase:
    """Create and query the SQLite database from the supplied CSV files."""

    DATABASE_NAME = "db.sqlite"
    QUESTION = "What is the total population of countries with English as their official language?"

    def __init__(self, csv_files: Sequence[str]) -> None:
        self.csv_files = csv_files
        with sqlite3.connect(self.DATABASE_NAME) as connection:
            self.import_csv_files(connection)
            population = self.english_official_population(connection)

        print(self.QUESTION)
        print(population)

    def import_csv_files(self, connection: sqlite3.Connection) -> None:
        """Create a table and import each CSV unless that table already exists."""
        for csv_file in self.csv_files:
            table_name = Path(csv_file).stem
            if self.table_exists(connection, table_name):
                continue

            with open(csv_file, newline="", encoding="utf-8-sig") as source:
                sample = source.read(8192)
                source.seek(0)
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                reader = csv.reader(source, dialect)
                try:
                    headers = next(reader)
                except StopIteration as error:
                    raise ValueError(f"{csv_file} is empty and has no header row") from error

                if not headers or any(not header for header in headers):
                    raise ValueError(f"{csv_file} must have non-empty column names")

                table_identifier = self.quote_identifier(table_name)
                column_definitions = ", ".join(
                    self.quote_identifier(header) for header in headers
                )
                placeholders = ", ".join("?" for _ in headers)
                insert_statement = (
                    f"INSERT INTO {table_identifier} VALUES ({placeholders})"
                )

                with connection:
                    connection.execute(
                        f"CREATE TABLE {table_identifier} ({column_definitions})"
                    )
                    connection.executemany(insert_statement, reader)

    @staticmethod
    def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
        """Return whether a table with this name is already present."""
        result = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table_name,),
        )
        return result.fetchone() is not None

    @staticmethod
    def quote_identifier(identifier: str) -> str:
        """Escape a SQLite identifier read from a filename or CSV header."""
        return '"' + identifier.replace('"', '""') + '"'

    @staticmethod
    def english_official_population(connection: sqlite3.Connection) -> int:
        """Sum populations for countries where English is an official language."""
        result = connection.execute(
            """
            SELECT COALESCE(SUM(CAST(country.Population AS INTEGER)), 0)
            FROM country
            JOIN countrylanguage
                ON country.Code = countrylanguage.CountryCode
            WHERE countrylanguage.Language = 'English'
                AND countrylanguage.IsOfficial = 'T'
            """
        )
        return result.fetchone()[0]


if __name__ == "__main__":
    WorldDatabase(sys.argv[1:])
