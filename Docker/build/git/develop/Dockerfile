############################################################
# Dockerfile to run libreosteo Containers
############################################################

FROM python:3.6-alpine as base
LABEL maintainer "Joseph Ligier"
ENV version 0.6-dev
ENV REPO Libreosteo
ENV USER libreosteo
ENV BRANCH develop

# Install dependancies
RUN apk add --update \
    tzdata \
    gettext \
    git \
    python3-dev \
    nodejs \
    nodejs-npm \
    gcc \
    libc-dev

RUN pip3 install wheel
ADD https://api.github.com/repos/$USER/$REPO/git/refs/heads/$BRANCH version.json
RUN git clone -b $BRANCH https://github.com/$USER/$REPO.git
RUN mkdir /svc
RUN cp Libreosteo/requirements/requirements.txt /svc

WORKDIR /svc
RUN pip3 wheel -r requirements.txt --wheel-dir=/svc/wheels

FROM python:3.6-alpine
ENV version 0.6-dev
ENV software Libreosteo
ENV REPO Libreosteo
ENV USER libreosteo
ENV BRANCH develop

COPY --from=base /svc /svc
COPY --from=base /Libreosteo /Libreosteo

RUN adduser -S -g '' libreosteo -u 1000
RUN chown -R libreosteo: /$software
COPY launch-libreosteo.sh /$software
RUN chmod a+x /$software/launch-libreosteo.sh

WORKDIR /svc
RUN pip install --no-index --find-links=wheels -r requirements.txt


# Install dependancies
RUN apk add --update \
    tzdata \
    gettext \
    git \
    nodejs \
    nodejs-npm

RUN npm install -g bower

USER $USER

# Install libreosteo
WORKDIR /$software

USER root
USER $USER

RUN bower install
RUN python3 manage.py collectstatic --noinput
COPY local.py.pg Libreosteo/settings/
COPY local.py.sqlite Libreosteo/settings/

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]

EXPOSE 8085

ENTRYPOINT ["./launch-libreosteo.sh"]

