FROM python:3.7-slim

RUN pip install telethon requests beautifulsoup4

COPY bin/* /app/

VOLUME data

CMD ["python", "-u", "/app/analyzeTrends.py"]
