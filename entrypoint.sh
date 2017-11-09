#!/bin/bash

ARGS=()

if [[ -n "$DOMAIN" ]]; then
    openssl req -x509 -newkey rsa:4096 \
        -days 365 -nodes \
        -keyout key.pem -out cert.pem \
        -subj "/CN=$DOMAIN"
    ARGS+=(--cert-file=cert.pem --key-file=key.pem)
fi

exec /server.py "$@" "${ARGS[@]}"
