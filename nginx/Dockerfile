FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
RUN rm /etc/nginx/nginx.conf
ADD sites-enabled/ /etc/nginx/sites-enabled
ADD nginx.conf /etc/nginx/nginx.conf
