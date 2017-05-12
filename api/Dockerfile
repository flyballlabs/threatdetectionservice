FROM alpine
RUN apk add --update git python3 mysql mysql-client
RUN git clone https://github.com/flyballlabs/threatdetectionservice.git
RUN cd threatdetectionservice/api
RUN /bin/sh -c ../server-setup.sh
RUN /bin/sh -c ../server-start.sh

