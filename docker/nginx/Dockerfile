FROM nginx:1.25

RUN rm ./etc/nginx/nginx.conf  && \
    rm -rf ./etc/nginx/conf.d/


COPY nginx.conf /etc/nginx/
COPY /conf.d /etc/nginx/conf.d
