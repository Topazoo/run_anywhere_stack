# pull official base image
FROM node:14.16.0-alpine as build

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY app/package.json ./
COPY app/package-lock.json ./
RUN npm install --no-package-lock && npm install react-scripts -g && npm install pusher-js -g

# add app
COPY ./app ./

# Had to throw these in to recompile sass to work on node:alpine
RUN apk add --no-cache python2 make g++
RUN npm uninstall node-sass && npm install node-sass@4.14.1 --sass-binary-name=linux_musl-x64-83

# build app
RUN npm run build

# start app
CMD ["npm", "start"]
