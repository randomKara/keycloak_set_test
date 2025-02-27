FROM httpd:2.4

RUN apt-get update && apt-get install -y --no-install-recommends procps


COPY ./conf/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./conf/httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf

RUN mkdir -p /usr/local/apache2/logs/custom && \
    mkdir -p /usr/local/apache2/run && \
    chown -R www-data:www-data /usr/local/apache2/logs /usr/local/apache2/run

USER www-data 