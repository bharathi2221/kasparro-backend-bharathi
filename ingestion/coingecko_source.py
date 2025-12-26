import requests
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import SessionLocal
from core.models import RawAPIData, NormalizedData, ETLCheckpoint
from schemas.data import APIRecord


API_URL = "https://api.coingecko.com/api/v3/coins/markets"
SOURCE_NAME = "coingecko"


def already_ingested(session: Session) -> bool:
    stmt = select(ETLCheckpoint).where(ETLCheckpoint.source == SOURCE_NAME)
    return session.execute(stmt).scalar_one_or_none() is not None


def ingest_coingecko():
    session: Session = SessionLocal()

    try:
        if already_ingested(session):
            print("CoinGecko already ingested. Skipping.")
            return

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1
        }

        response = requests.get(API_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        session.add(RawAPIData(source=SOURCE_NAME, payload=data))

        for coin in data:
            record = APIRecord(
                record_id=coin["id"],
                name=coin["name"],
                value=str(coin["current_price"])
            )

            session.add(
                NormalizedData(
                    record_id=record.record_id,
                    name=record.name,
                    value=record.value,
                    source=SOURCE_NAME
                )
            )

        session.add(ETLCheckpoint(source=SOURCE_NAME))
        session.commit()

        print(f"Ingested {len(data)} CoinGecko records")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    ingest_coingecko()
