import requests
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import SessionLocal
from core.models import RawAPIData, NormalizedData, ETLCheckpoint
from schemas.data import APIRecord


API_URL = "https://api.coinpaprika.com/v1/tickers"
SOURCE_NAME = "coinpaprika"


def already_ingested(session: Session) -> bool:
    stmt = select(ETLCheckpoint).where(ETLCheckpoint.source == SOURCE_NAME)
    return session.execute(stmt).scalar_one_or_none() is not None


def ingest_coinpaprika():
    session: Session = SessionLocal()

    try:
        # Incremental check
        if already_ingested(session):
            print("CoinPaprika already ingested. Skipping.")
            return

        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        data = response.json()

        # Store raw payload
        session.add(RawAPIData(source=SOURCE_NAME, payload=data))

        # Normalize minimal required fields
        for coin in data:
            record = APIRecord(
                record_id=coin["id"],
                name=coin["name"],
                value=str(coin["quotes"]["USD"]["price"])
            )

            session.add(
                NormalizedData(
                    record_id=record.record_id,
                    name=record.name,
                    value=record.value,
                    source=SOURCE_NAME
                )
            )

        # Save checkpoint
        session.add(ETLCheckpoint(source=SOURCE_NAME))
        session.commit()

        print(f"Ingested {len(data)} CoinPaprika records")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    ingest_coinpaprika()
