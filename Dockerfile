FROM python:3.10-slim-bookworm
LABEL maintainer="Eric Kuo <as2229181@gmailc.om>"

RUN apt-get update \
    && apt-get install -y --no-install-recommends vim \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Env
ENV PYTHONPATH="/app"
ENV ENV="/root/.bashrc"

# Prepare packages
ARG PRODUCT_NAME="app"
WORKDIR /${PRODUCT_NAME}
RUN mkdir -p /${PRODUCT_NAME}
COPY requirements.txt .

# Install requirement
RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt

# Vim
RUN echo "set ts=4" >> /etc/vim/vimrc
RUN echo "set sw=4" >> /etc/vim/vimrc
RUN echo "set expandtab" >> /etc/vim/vimrc
RUN echo "set hls" >> /etc/vim/vimrc

RUN /bin/sh -c echo 'alias python="python3"' >> /root/.bashrc
RUN /bin/sh -c echo 'alias pip="python3 -m pip"' >> /root/.bashrc

# alias
RUN alias la="ls -A"
RUN alias l="ls -CF"

RUN echo 'alias run="python main.py line_bot"' >> /root/.bashrc
