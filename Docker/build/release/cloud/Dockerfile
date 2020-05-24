ARG python_version=3.6
FROM python:${python_version} as base
ENV software Libreosteo
ENV version 0.6.0
ENV REPO Libreosteo
ENV USER libreosteo
ENV BRANCH develop

# Install dependancies
#RUN apt-get install -y postgresql-libs gettext git nodejs nodejs-npm tzdata yarn postgresql-dev

RUN pip install wheel

# Retrieve Libreosteo sources
ADD https://github.com/libreosteo/Libreosteo/archive/${version}.tar.gz /
RUN tar xvf 0.6.0.tar.gz && mv Libreosteo-${version} $software

# Create pip packages
RUN mkdir /svc
RUN cp /$software/requirements/requirements.txt /svc
WORKDIR /svc
RUN pip wheel -r requirements.txt --wheel-dir=/svc/wheels
RUN pip wheel psycopg2 --wheel-dir=/svc/wheels


# Install Javascript dependancies
FROM python:${python_version} as javascript
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn
RUN useradd -ms /bin/sh -u 1000 libreosteo
COPY --from=base --chown=libreosteo:1000 /Libreosteo /Libreosteo
USER libreosteo
WORKDIR /Libreosteo
ADD package.json .
RUN yarn

# Final Image
FROM python:${python_version}
LABEL maintainer "Joseph Ligier"
ENV debug False
ENV sql_host db
ENV sql_port 5432
ENV sql_name postgres
ENV sql_user postgres

# Install dependancies
#RUN apk add --no-cache tzdata

# Install pip dependancies
COPY --from=base /svc /svc
WORKDIR /svc
RUN pip install --no-index --find-links=wheels -r requirements.txt && pip install --no-index --find-links=wheels psycopg2  && rm -rf /svc

# Retrieve Libreosteo dir
RUN useradd -ms /bin/sh -u 1000 libreosteo
COPY --from=javascript --chown=libreosteo:1000 /Libreosteo /Libreosteo
ADD django-secret-key /usr/local/bin/

# Prepare Libreosteo instance
USER libreosteo
WORKDIR /Libreosteo
RUN rm /Libreosteo/libreosteoweb/static/components/moment/meteor/moment.js
RUN python manage.py collectstatic --noinput

# Customize /Libreosteo dir for docker
COPY launch-libreosteo.sh /Libreosteo
USER root
RUN chmod a+x /Libreosteo/launch-libreosteo.sh
USER libreosteo
COPY local.py.pg /Libreosteo/Libreosteo/settings/
COPY local.py.sqlite /Libreosteo/Libreosteo/settings/

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]
EXPOSE 8085
ENTRYPOINT ["./launch-libreosteo.sh"]
