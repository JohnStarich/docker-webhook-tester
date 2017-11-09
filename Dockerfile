FROM python:2

COPY entrypoint.sh /
COPY server.py /

ENTRYPOINT ["/entrypoint.sh"]
