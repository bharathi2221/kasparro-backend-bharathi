# Backend & ETL System

## Overview
This project implements a backend and ETL system that ingests data from
multiple sources (API and CSV), stores raw data, normalizes it into a unified
schema, and exposes it via a REST API.

The system is designed to be incremental, idempotent, and easily deployable, and ingests cryptocurrency data from CoinPaprika and CoinGecko APIs.

---

## Architecture

- **PostgreSQL**: Raw and normalized data storage
- **ETL Layer**:
  - API ingestion
  - CSV ingestion
  - Incremental checkpointing
- **Backend API**:
  - FastAPI
  - Pagination, filtering, metadata
- **Validation**:
  - Pydantic schemas
- **Testing**:
  - pytest (ETL, API, failure scenarios)

---

## Project Structure
- backend-etl-system/
    |── api/
    ├── ingestion/
    ├── schemas/
    ├── core/
    ├── tests/
    ├── docker-compose.yml
    ├── README.md
    ├── requirements.txt

---

## Install dependencies
```bash 
pip install -r requirements.txt
```

## Setup & Run

### 1. Start PostgreSQL
```bash
docker compose up -d
```

### 2. Activate Python environment
```bash
venv\Scripts\activate
```

### 3. Initialize database
```bash
python -m core.init_db
```

### 4. Run ETL jobs
```bash
python -m ingestion.coinpaprika_source
python -m ingestion.coingecko_source
```

### 5. Start API
```bash
uvicorn api.main:app --reload
```

## API Endpoints
### Health
GET /health

### Data
GET /data?source=<source>&limit=10&offset=0

## Tests
```bash
pytest
```