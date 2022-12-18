FROM python:buster
ADD . .
WORKDIR .
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm install --global yarn
RUN yarn install
RUN set -ex; \
    yarn cache clean; \
    yarn run build
CMD ["yarn", "run", "start"]