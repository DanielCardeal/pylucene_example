FROM eclipse-temurin:17

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

VOLUME /src/examples

# Install dependencies
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		python3-dev python3-venv python3-setuptools \
		build-essential \
		subversion \
	&& rm -rf /var/lib/apt/lists/*

# Download JCC source code
WORKDIR /src
RUN svn co https://svn.apache.org/repos/asf/lucene/pylucene/trunk/jcc jcc

# Build and install JCC
WORKDIR /src/jcc
ENV JCC_JDK /opt/java/openjdk/
RUN ln -sf /opt/java/openjdk/ /opt/java/openjdk/jre \
	&& ln -sf /opt/java/openjdk/lib /opt/java/openjdk/lib/amd64 \
	&& python3 setup.py build \
	&& python3 setup.py install \
	|| exit 1

# Download Pylucene source
WORKDIR /src
RUN wget -q https://dlcdn.apache.org/lucene/pylucene/pylucene-9.1.0-src.tar.gz \
	&& wget -qO - https://dlcdn.apache.org/lucene/pylucene/pylucene-9.1.0-src.tar.gz.sha256 \
	| sha256sum -c \
	&& tar -xf pylucene-9.1.0-src.tar.gz \
	&& rm pylucene-9.1.0-src.tar.gz \
	|| exit 1

# Compile, test and install Pylucene
WORKDIR /src/pylucene-9.1.0
COPY Makefile-mod Makefile
RUN make && make test && make install
