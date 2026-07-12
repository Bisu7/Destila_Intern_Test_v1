FROM python:3.10-slim
WORKDIR /app

RUN pip install fastapi uvicorn sqlalchemy pandas pydantic

COPY . /app/

RUN python backend/ingest.py && python backend/detect_exceptions.py

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
