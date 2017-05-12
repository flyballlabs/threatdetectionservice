FROM alpine
RUN git clone git@github.com:flyballlabs/threatdetectionservice.git
RUN cd threatdetectionservice/api
RUN apk add mysql mysql-client
RUN ../server-setup.sh
RUN ../server-start.sh

