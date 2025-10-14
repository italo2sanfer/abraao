FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install -y vim git build-essential \
    python3-dev python3-setuptools libldap2-dev libsasl2-dev \
    zlib1g-dev libxmlsec1-dev libblas-dev liblapack-dev default-mysql-client \
    libssl-dev libffi-dev poppler-utils locales postgresql-client iputils-ping
RUN pip install --upgrade pip

RUN locale-gen
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt
ENV LC_ALL=pt_BR.UTF-8

RUN adduser --disabled-password dev
USER dev
WORKDIR /home/dev/code
ENV PATH="/home/dev/.local/bin:${PATH}"
RUN git config --global url."https://".insteadOf git://

ADD --chown=dev:dev requirements/ ./requirements
RUN pip install -r requirements/development.txt