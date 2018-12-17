FROM ubuntu:18.04

LABEL maintainer Alexander Merck <alexander.t.merck@gmail.com>
LABEL name "cowrie"
LABEL version "0.2"
LABEL release "1"
LABEL summary "Cowrie HoneyPot container"
LABEL description "Cowrie is a medium interaction SSH and Telnet honeypot designed to log brute force attacks and the shell interaction performed by the attacker."
LABEL authoritative-source-url "https://github.com/CommunityHoneyNetwork/communityhoneynetwork"
LABEL changelog-url "https://github.com/CommunityHoneyNetwork/communityhoneynetwork/commits/master"

# Set DOCKER var - used by Cowrie init to determine logging
ENV DOCKER "yes"
ENV COWRIE_GROUP "cowrie"
ENV COWRIE_USER "cowrie"
ENV COWRIE_DIR "/opt"

RUN apt-get update \
      && apt-get install -y python-apt gettext-base

RUN apt-get install -y git jq python-virtualenv libmpfr-dev \
    libssl-dev libmpc-dev libffi-dev \
    build-essential libpython-dev python2.7-minimal \
    python-pip authbind runit

RUN groupadd -r -g 1000 ${COWRIE_GROUP} && \
    useradd -r -u 1000 -m -g ${COWRIE_GROUP} ${COWRIE_USER}

WORKDIR ${COWRIE_DIR}

RUN git clone https://github.com/cowrie/cowrie.git

# Upgrade pip and setup tools
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools

# Install repository dependencies
RUN pip install --no-cache-dir --upgrade -r ${COWRIE_DIR}/cowrie/requirements.txt
RUN pip install --no-cache-dir --upgrade pika requests fluent-logger

COPY plugins/stingarfluentd.py ${COWRIE_DIR}/cowrie/src/cowrie/output

# Build config file
COPY cowrie.cfg.template ${COWRIE_DIR}
#RUN envsubst < cowrie.cfg.template > cowrie/etc/cowrie.cfg

# Set permissions on cowrie directory
RUN chown -R ${COWRIE_USER} ${COWRIE_DIR}

# Do this for containers only
RUN sed -i 's/^DAEMONIZE=""/DAEMONIZE="-n"/' /opt/cowrie/bin/cowrie

USER ${COWRIE_USER}
ENV PATH=${COWRIE_DIR}/cowrie/bin:${PATH}
CMD envsubst < cowrie.cfg.template > cowrie/etc/cowrie.cfg \
    && cowrie start -n --pidfile=var/run/cowrie.pid]
EXPOSE 2222 2223