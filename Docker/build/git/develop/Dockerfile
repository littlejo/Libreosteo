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
    gcc \
    libc-dev

RUN npm install -g bower

RUN pip install wheel
ADD https://api.github.com/repos/$USER/$REPO/git/refs/heads/$BRANCH version.json
RUN git clone -b $BRANCH https://github.com/$USER/$REPO.git

COPY launch-libreosteo.sh /$software
RUN chmod a+x /$software/launch-libreosteo.sh
COPY local.py.pg /$software/$software/settings/
COPY local.py.sqlite /$software/$software/settings/

RUN mkdir /svc
RUN cp /Libreosteo/requirements/requirements.txt /svc

WORKDIR /svc
RUN pip wheel -r requirements.txt --wheel-dir=/svc/wheels

RUN adduser -S -g '' libreosteo -u 1000
RUN chown -R libreosteo: /$software

USER libreosteo

WORKDIR /$software
RUN bower install

FROM python:3.6-alpine
LABEL maintainer "Joseph Ligier"

COPY --from=base /svc /svc
COPY --from=base /Libreosteo /Libreosteo

RUN adduser -S -g '' libreosteo -u 1000

WORKDIR /svc
RUN pip install --no-index --find-links=wheels -r requirements.txt

# Install dependancies
RUN apk add --update \
    tzdata \
    gettext \
    nodejs

RUN chown libreosteo: /Libreosteo /Libreosteo/* /Libreosteo/Libreosteo/settings/

RUN rm -rf /svc
USER libreosteo

WORKDIR /Libreosteo
RUN python manage.py collectstatic --noinput

VOLUME ["/Libreosteo/media", "/Libreosteo/sql"]

EXPOSE 8085

ENTRYPOINT ["./launch-libreosteo.sh"]
