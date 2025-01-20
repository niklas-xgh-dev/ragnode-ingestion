# Ragnode-Ingestion

Lightweight scheduler for RAG data ingestion into PostgreSQL vector store.

```
ragnode-ingestion/
├── app/src/           
│   ├── core/          # Core utilities
│   ├── database.py    # PostgreSQL + pgvector
│   ├── fetch/         # Data fetchers
│   ├── ingest/        # Ingestion pipeline
│   ├── models/        # Data models
│   └── tasks/         # Scheduled tasks
├── Dockerfile        
└── main.py           
```

## Stack
- Python 3.12, Docker
- PostgreSQL (RDS) + pgvector
- Apache Airflow 2.7
- Embeddings (Model TBD)
- SQLAlchemy 2.0 + asyncpg

Logs output to stdout/stderr for container monitoring.