FROM python:3-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LOG_LEVEL=INFO

COPY ./src /snapshot

RUN pip3 install --upgrade pip && \
    pip3 install -r /snapshot/requirements.txt

CMD ["python3", "/snapshot/main.py"]