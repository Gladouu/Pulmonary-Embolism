# https://www.youtube.com/watch?v=FrKccQUeaUE

FROM mysql:8.0

EXPOSE 3306

ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

ENV MYSQL_DATABASE=${MYSQL_DATABASE}

COPY ./pe_api.sql /docker-entrypoint-initdb.d/