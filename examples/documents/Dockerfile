FROM pypy:3

VOLUME /src/examples/documents

WORKDIR /src/examples/documents

RUN apt-get install -y --no-install-recommends libdb-dev

ENV BERKELEYDB_DIR=/usr

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
