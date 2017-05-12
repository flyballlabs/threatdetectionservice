FROM alpine
RUN apk add git python3 mysql mysql-client
RUN git clone git@github.com:flyballlabs/threatdetectionservice.git
RUN cd threatdetectionservice/api
RUN ../server-setup.sh
RUN ../server-start.sh

