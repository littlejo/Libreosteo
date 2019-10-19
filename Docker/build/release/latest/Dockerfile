ARG python_version=3.6
FROM python:${python_version}-alpine as base
ENV software Libreosteo
ENV version 0.6.0
ENV REPO Libreosteo
ENV USER libreosteo
ENV BRANCH develop

# Install dependancies
RUN apk add --no-cache \
    gettext \
    git \
    gcc \
    linux-headers \
    libc-dev \
    nodejs \
    nodejs-npm \
    tzdata \
    yarn

RUN pip install wheel

# Retrieve Libreosteo sources
ADD https://github.com/libreosteo/Libreosteo/archive/${version}.tar.gz /
RUN tar xvf 0.6.0.tar.gz && mv Libreosteo-${version} $software

# Create pip packages
RUN mkdir /svc
RUN cp /$software/requirements/requirements.txt /svc
WORKDIR /svc
RUN pip wheel -r requirements.txt --wheel-dir=/svc/wheels

# Customize /Libreosteo dir for docker
COPY launch-libreosteo.sh /$software
RUN chmod a+x /$software/launch-libreosteo.sh
COPY local.py.pg /$software/$software/settings/
COPY local.py.sqlite /$software/$software/settings/

# Install Javascript dependancies
RUN adduser -S -g '' libreosteo -u 1000
RUN chown -R libreosteo: /$software
USER libreosteo
WORKDIR /$software
RUN yarn

# Final Image
FROM python:${python_version}-alpine
LABEL maintainer "Joseph Ligier"
ENV debug False
ENV sql_host db
ENV sql_port 5432
ENV sql_name postgres
ENV sql_user postgres

# Install dependancies
RUN apk add --no-cache tzdata

# Install pip dependancies
COPY --from=base /svc /svc
WORKDIR /svc
RUN pip install --no-index --find-links=wheels -r requirements.txt && rm -rf /svc

# Retrieve Libreosteo dir
RUN adduser -S -g '' libreosteo -u 1000
COPY --from=base --chown=libreosteo:1000 /Libreosteo /Libreosteo
ADD django-secret-key /usr/local/bin/

# Prepare Libreosteo instance
USER libreosteo
WORKDIR /Libreosteo
RUN python manage.py collectstatic --noinput

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]
EXPOSE 8085
ENTRYPOINT ["./launch-libreosteo.sh"]
