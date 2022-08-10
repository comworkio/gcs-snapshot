FROM python:3-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LOG_LEVEL=INFO \
    GCS_DEST_DATE_FORMAT=%Y%m%d \
    MAX_RETRY=5

COPY ./src /snapshot

RUN pip3 install --upgrade pip && \
    pip3 install -r /snapshot/requirements.txt

CMD ["python3", "/snapshot/main.py"]
