FROM python:3.6-alpine as base
ENV software Libreosteo
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
    linux-headers \
    gcc \
    libc-dev

RUN npm install -g bower
RUN pip install wheel

# Retrieve Libreosteo sources
ADD https://api.github.com/repos/$USER/$REPO/git/refs/heads/$BRANCH version.json
RUN git clone -b $BRANCH https://github.com/$USER/$REPO.git

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
RUN bower install

# Final Image
FROM python:3.6-alpine
LABEL maintainer "Joseph Ligier"

# Install dependancies
RUN apk add --update \
    tzdata \
    gettext \
    nodejs

# Install pip dependancies
COPY --from=base /svc /svc
WORKDIR /svc
RUN pip install --no-index --find-links=wheels -r requirements.txt && rm -rf /svc

# Retrieve Libreosteo dir
RUN adduser -S -g '' libreosteo -u 1000
COPY --from=base /Libreosteo /Libreosteo
RUN chown libreosteo: /Libreosteo /Libreosteo/* /Libreosteo/Libreosteo/settings/

# Prepare Libreosteo instance
USER libreosteo
WORKDIR /Libreosteo
RUN python manage.py collectstatic --noinput

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]
EXPOSE 8085
ENTRYPOINT ["./launch-libreosteo.sh"]
