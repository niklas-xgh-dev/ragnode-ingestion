docker build -t ragnode-ingestion .      
docker run -p 8000:8000 --env-file .env ragnode-ingestion