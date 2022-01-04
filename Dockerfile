FROM redhat/ubi8

ARG PROJECT_ROOT=/root
ARG USER_TIMEZONE=Europe/Zurich
ARG USER_COUNTRY=CH
ARG USER_LANGUAGE=fr
ARG FILE_ENCODING=UTF-8

LABEL \
    MAINTAINER=metairie \
    USER_TIMEZONE=${USER_TIMEZONE} \
    USER_COUNTRY=${USER_COUNTRY} \
    USER_LANGUAGE=${USER_LANGUAGE} \
    FILE_ENCODING=${FILE_ENCODING}

ENV \
# Project info + Timezone + Lang + encoding info
    API_HOST=${API_HOST} \
    API_PORT=${API_PORT} \
    TZ=${USER_TIMEZONE} \
    LANGUAGE=${USER_LANGUAGE}_${USER_COUNTRY}:${FILE_ENCODING} \
    LANG=${USER_LANGUAGE}_${USER_COUNTRY}.${FILE_ENCODING} \
    USER_TIMEZONE=${USER_TIMEZONE} \
    USER_COUNTRY=${USER_COUNTRY} \
    USER_LANGUAGE=${USER_LANGUAGE} \
    HTTPS_PROXY_HOST=${HTTPS_PROXY_HOST} \
    HTTPS_PROXY_PORT=${HTTPS_PROXY_PORT}

# update image
RUN dnf -y upgrade && dnf -y install python39 python39-devel wget git
ADD requirements.txt /root/
RUN pip3 install --user --no-cache-dir -r ${PROJECT_ROOT}/requirements.txt

EXPOSE ${API_PORT}
ADD main.py ${PROJECT_ROOT}/main.py
ADD static ${PROJECT_ROOT}/static 
WORKDIR ${PROJECT_ROOT}
ENV PATH="/root/.local/bin:${PATH}"
CMD uvicorn main:app --host 0.0.0.0 --port 8000
