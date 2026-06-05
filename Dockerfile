FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app

RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]