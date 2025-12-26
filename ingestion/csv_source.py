import csv
from pathlib import Path
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.models import RawCSVData, NormalizedData
from schemas.data import CSVRecord


CSV_PATH = Path("data/sample.csv")
SOURCE_NAME = "local_csv"


def read_csv() -> list[dict]:
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def ingest_csv_data():
    session: Session = SessionLocal()

    try:
        rows = read_csv()

        # 1. Store raw CSV payload
        raw_entry = RawCSVData(
            source=SOURCE_NAME,
            payload=rows
        )
        session.add(raw_entry)

        # 2. Normalize records
        for row in rows:
            validated = CSVRecord(
                record_id=row["record_id"],
                name=row.get("name"),
                value=row.get("value"),
            )

            normalized = NormalizedData(
                record_id=validated.record_id,
                name=validated.name,
                value=validated.value,
                source=SOURCE_NAME
            )
            session.add(normalized)

        session.commit()
        print(f"Ingested {len(rows)} CSV records successfully.")

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


if __name__ == "__main__":
    ingest_csv_data()
