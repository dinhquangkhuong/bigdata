FROM prestodb/presto:latest
# voldern/presto:latest

# RUN <<EOF
# mkdir -p /etc/catalog
# EOF
# voldern/presto:latest
COPY cassandra.properties /opt/presto/etc/catalog/
COPY cassandra.properties /etc/catalog/
# COPY container/presto/ /etc
