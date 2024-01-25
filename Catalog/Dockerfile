FROM python:3-alpine3.12
WORKDIR /catalog
COPY /Catalog/catalog.py /catalog
COPY /utils/ /catalog/utils/
COPY /Catalog/requirements.txt /catalog
RUN python -m pip install -r requirements.txt
EXPOSE 5000
ARG VIDEO_SERVER
ARG DATABASE
RUN echo "Video server address: $VIDEO_SERVER"
RUN echo "Database address: $DATABASE"
ENTRYPOINT [ "python", "./catalog.py" ]
CMD ["-d", "-s", "http://localhost:80", "-b", "http://172.16.0.3:8080"]
