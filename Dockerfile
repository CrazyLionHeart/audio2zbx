FROM python:3-slim AS compile-image

# -----------------------------------------------------------------------------

ARG BUILD_DATE
ARG BUILD_VERSION

ENV DEBIAN_FRONTEND noninteractive

LABEL \
  version="${BUILD_VERSION}" \
  maintainer="Alexander Sytar <sytar.alex@gmail.com>" \
  org.label-schema.build-date=${BUILD_DATE} \
  org.opencontainers.image.created=${BUILD_DATE} \
  org.opencontainers.image.authors="Alexander Sytar <sytar.alex@gmail.com>" \
  org.opencontainers.image.url="https://github.com" \
  org.opencontainers.image.version="${BUILD_VERSION}" \
  org.opencontainers.image.licenses="MIT" \
  org.opencontainers.image.title="Zoom Statistic Reciever" \
  org.opencontainers.image.description="Recieve Zoom Statistice from CyberSecure SBRF"


# -----------------------------------------------------------------------------

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt \  
  && rm -Rf /root/.cache \
  && find . -type d -name __pycache__ -exec rm -r {} \+


FROM python:3-slim AS build-image

ENV PYTHONUNBUFFERED 1
# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

COPY ./main.py ./docker-entrypoint.sh ./
COPY --from=compile-image /root/.local /root/.local

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    dumb-init \
    procps \
  && chmod +x /app/docker-entrypoint.sh

CMD ["/usr/bin/dumb-init", "/bin/bash", "/app/docker-entrypoint.sh"]

HEALTHCHECK \
  --interval=5s \
  --timeout=2s \
  --retries=12 \
  CMD ps ax | grep -v grep | grep -c main.py || false