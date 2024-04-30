FROM apache/superset

ENV SUPERSET_SECRET_KEY=Lr/mxr3VVkuUG/D/0zy+SPPp5zfpRooEHUdDfEdRNlZAzi1Q+Z3v68y3
ENV FLASK_APP=superset

RUN superset db upgrade
RUN superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

RUN superset init

# superset run -p 8088 --with-threads --reload --debugger
CMD ["superset", "run", "-p", "8088", "--with-threads", "--reload", "--debugger"]

