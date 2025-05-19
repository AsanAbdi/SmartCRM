FROM python:3.12-slim

WORKDIR /SmartCRM

RUN apt-get update && apt-get install -y netcat-openbsd curl && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:."

COPY . .

CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]
