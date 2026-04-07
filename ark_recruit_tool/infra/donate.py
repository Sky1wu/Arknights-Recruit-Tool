from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DonationRecord:
    date: str
    amount: str
    name: str


class DonationRepository:
    def __init__(self, csv_path: Path) -> None:
        self._csv_path = csv_path

    def list_records(self) -> tuple[DonationRecord, ...]:
        if not self._csv_path.exists():
            return ()

        records: list[DonationRecord] = []
        with self._csv_path.open("r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3:
                    continue
                records.append(DonationRecord(date=row[0], amount=row[1], name=row[2]))
        return tuple(records)
