"""Command-line entry point for text-file processing."""

from pathlib import Path


class Texter:
    """Process a text file."""

    def __init__(self, file_name):
        self.file_name = file_name

    def run(self):
        """Print the character and capital-letter counts."""
        with open(self.file_name, encoding="utf-8") as text_file:
            text = text_file.read()

        print("Number of all characters:", len(text))
        print(
            "Number of capital letters:",
            sum(character.isupper() for character in text),
        )


def main():
    Texter(Path(__file__).with_name("test.txt")).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())