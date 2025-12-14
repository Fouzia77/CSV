
"""
Custom CSV reader and writer implemented from scratch.

Features:
- Comma-delimited fields
- Double-quoted fields
- Escaped double quotes ("")
- Embedded newlines inside quoted fields
- Streaming reading: one row at a time
"""

from typing import Iterable, List, TextIO


class CustomCsvReader:
    """
    Custom CSV reader that parses comma-separated values with support for:
    - quoted fields
    - escaped quotes ("")
    - embedded newlines inside quoted fields

    Works as an iterator over rows (lists of strings).
    """

    def __init__(self, file_obj: TextIO, delimiter: str = ",", quotechar: str = '"'):
        self.file = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self._eof = False

    def __iter__(self):
        return self

    def __next__(self) -> List[str]:
        if self._eof:
            raise StopIteration

        row: List[str] = []
        field_chars: List[str] = []
        in_quotes = False

        while True:
            ch = self.file.read(1)
            
            if ch == "":
                self._eof = True
                if field_chars or row:
                    row.append("".join(field_chars))
                    return row
                raise StopIteration


            if ch == self.quotechar:
                if not in_quotes:
                  
                    in_quotes = True
                else:
                  
                    next_ch = self.file.read(1)
                    if next_ch == self.quotechar:
                        field_chars.append(self.quotechar)
                    else:
                        in_quotes = False
                        ch = next_ch
                        if ch == "":
                            self._eof = True
                            row.append("".join(field_chars))
                            return row
                if in_quotes:
                    continue

          
            if in_quotes:
                field_chars.append(ch)
                continue

           
            if ch == self.delimiter:
                row.append("".join(field_chars))
                field_chars = []
            elif ch == "\n":
                row.append("".join(field_chars))
                return row
            elif ch == "\r":
                next_ch = self.file.read(1)
                if next_ch not in ("\n", ""):
                    field_chars.append(next_ch)
                row.append("".join(field_chars))
                return row
            else:
                field_chars.append(ch)


class CustomCsvWriter:
    """
    Custom CSV writer that writes CSV rows and escapes fields properly.
    """
    
    def __init__(
        self,
        file_obj: TextIO,
        delimiter: str = ",",
        quotechar: str = '"',
        lineterminator: str = "\r\n",
    ):
        self.file = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.lineterminator = lineterminator

    def _quote_field(self, field: str) -> str:
        if not isinstance(field, str):
            field = str(field)

        needs_quotes = (
            self.delimiter in field
            or self.quotechar in field
            or "\n" in field
            or "\r" in field
        )

        if needs_quotes:
            escaped = field.replace(self.quotechar, self.quotechar * 2)
            return f'{self.quotechar}{escaped}{self.quotechar}'

        return field

    def writerow(self, row: Iterable[str]) -> None:
        fields = [self._quote_field(f) for f in row]
        line = self.delimiter.join(fields) + self.lineterminator
        self.file.write(line)

    def writerows(self, rows: Iterable[Iterable[str]]) -> None:
        for row in rows:
            self.writerow(row)
