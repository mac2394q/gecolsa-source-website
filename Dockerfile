FROM python:3.6

RUN apt update && apt install -y libproj-dev gdal-bin \
    && apt autoremove -y --purge \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/
RUN wget https://nodejs.org/dist/v10.13.0/node-v10.13.0-linux-x64.tar.xz \
    && tar xvf node-v10.13.0-linux-x64.tar.xz \
    && cp -rp node-v10.13.0-linux-x64/* /usr/local/ \
    && rm -rf node-v10.13.0-linux-x64.tar.xz node-v10.13.0-linux-x64/

WORKDIR /usr/local/lib/
RUN wget https://github.com/sass/libsass/archive/3.5.4.tar.gz \
    && tar xvzf 3.5.4.tar.gz && rm 3.5.4.tar.gz
ENV SASS_LIBSASS_PATH "/usr/local/lib/libsass-3.5.4"

RUN echo 'SASS_LIBSASS_PATH="/usr/local/lib/libsass-3.5.4"' >> /etc/environment
RUN wget https://github.com/sass/sassc/archive/3.5.0.tar.gz \
    && tar xvzf 3.5.0.tar.gz && rm 3.5.0.tar.gz
WORKDIR /usr/local/lib/sassc-3.5.0/
RUN make && ln -s /usr/local/lib/sassc-3.5.0/bin/sassc /usr/local/bin/sassc

RUN npm install gulp-cli -g

RUN curl -o- -L https://yarnpkg.com/install.sh | bash -s -- --version 1.12.3
RUN ln -s /root/.yarn/bin/yarn /usr/local/bin/yarn

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
