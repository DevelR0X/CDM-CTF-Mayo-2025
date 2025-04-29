FROM php:8.2-apache

COPY ./src /var/www/html/

ENV DB_NAME=database.db
ENV DB_PATH=/var/www/html/$DB_NAME

RUN sh -c '[ -f "$DB_PATH" ] && rm "$DB_PATH" || echo "Archivo $DB_PATH no existe"'

RUN chown -R www-data:www-data /var/www/html

EXPOSE 80
