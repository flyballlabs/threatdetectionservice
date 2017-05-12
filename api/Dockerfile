FROM alpine
RUN apk add --update git python3 mysql mysql-client
RUN git clone https://github.com/flyballlabs/threatdetectionservice.git
RUN cd threatdetectionservice/api
RUN ../server-setup.sh
RUN ../server-start.sh

