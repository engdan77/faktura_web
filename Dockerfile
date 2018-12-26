# based on https://hub.docker.com/r/kiki407/alpine-web2py
FROM nginx:stable-alpine

ENV PW admin
ENV INSTALL_DIR /home/nginx
ENV WEB2PY_DIR $INSTALL_DIR/web2py
ENV CERT_PASS web2py

WORKDIR $INSTALL_DIR

EXPOSE 80 443 8000

RUN apk update && \
apk add --no-cache --virtual=build-dependencies \
linux-headers \
sudo \
make \
cmake \
gcc \
g++ \
openssl \
wget \
tzdata \
python3 \
python3-dev \
pcre-dev \
supervisor

RUN	pip3 install setuptools --upgrade && \
pip3 install --upgrade pip && \
PIPPATH=`which pip` && \
$PIPPATH install --upgrade uwsgi && \
mkdir /etc/nginx/conf.d/web2py

RUN mkdir /etc/nginx/sites-available/
RUN mkdir /etc/nginx/sites-enabled/
ADD ../../../docker_files/gzip_static.conf /etc/nginx/conf.d/web2py/gzip_static.conf
ADD ../../../docker_files/gzip.conf /etc/nginx/conf.d/web2py/gzip.conf
ADD ../../../docker_files/web2py.conf /etc/nginx/conf.d/

RUN rm /etc/nginx/conf.d/default.conf && \
mkdir /etc/nginx/ssl && cd /etc/nginx/ssl && \
openssl genrsa -passout pass:$CERT_PASS 1024 > web2py.key && \
chmod 400 web2py.key && \
openssl req -new -x509 -nodes -sha1 -days 1780 -subj "/C=IE/ST=Denial/L=Galway/O=kiki407/CN=www.example.com" -key web2py.key > web2py.crt && \
openssl x509 -noout -fingerprint -text < web2py.crt > web2py.info && \
mkdir /etc/uwsgi && \
mkdir /var/log/uwsgi

ADD ../../../docker_files/web2py.ini /etc/uwsgi/web2py.ini

ADD ../../../docker_files/supervisor-app.ini /etc/supervisor.d/

RUN cd $INSTALL_DIR && \
wget http://web2py.com/examples/static/web2py_src.zip && \
unzip web2py_src.zip && \
rm web2py_src.zip && \
mv web2py/handlers/wsgihandler.py web2py/wsgihandler.py && \
chown -R nginx:nginx web2py && \
cd $WEB2PY_DIR && \
sudo -u nginx python -c "from gluon.main import save_password; save_password('$PW',80)" && \
sudo -u nginx python -c "from gluon.main import save_password; save_password('$PW',443)" && \
sudo nginx

USER root

RUN cp -r web2py/applications/welcome web2py/applications/faktura_web
ADD models web2py/applications/faktura_web/models
ADD controllers web2py/applications/faktura_web/controllers
ADD views web2py/applications/faktura_web/views
ADD modules web2py/applications/faktura_web/modules
ADD private web2py/applications/faktura_web/private

RUN find web2py/applications/faktura_web/ -iname *.pyc -exec rm {} \;
RUN chown -R nginx:nginx web2py/applications/faktura_web/

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip install reportlab

CMD ["supervisord", "-n"]