FROM edoburu/pgbouncer:v1.24.1-p0

USER root

RUN apk update && \
    apk add --no-cache \
        dos2unix \
        bash && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /commands

COPY ./commands/setup_pgbouncer_auth.sh /commands/setup_pgbouncer_auth.sh

RUN dos2unix /commands/*.sh

RUN chmod +x /commands/*.sh

RUN echo '#!/bin/sh' > /commands/entrypoint_wrapper.sh && \
    echo '/commands/setup_pgbouncer_auth.sh' >> /commands/entrypoint_wrapper.sh && \
    echo 'exec su postgres -c "pgbouncer /etc/pgbouncer/pgbouncer.ini"' >> /commands/entrypoint_wrapper.sh && \
    chmod +x /commands/entrypoint_wrapper.sh


ENTRYPOINT ["/commands/entrypoint_wrapper.sh"]