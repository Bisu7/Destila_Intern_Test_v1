FROM python:3.10-slim
WORKDIR /app

# Install dependencies directly
RUN pip install fastapi uvicorn sqlalchemy pandas pydantic

# Copy the entire project so ingest scripts can find candidate_pack/data/
COPY . /app/

# Generate the SQLite database during the image build
RUN python backend/ingest.py && python backend/detect_exceptions.py

# Start the FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
