FROM python:3.8-alpine
LABEL maintainer="Sungwon Jung"
WORKDIR /usr/work
COPY ./techtrends/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./techtrends/ ./
RUN python init_db.py
RUN pip install -r requirements.txt
EXPOSE 3111
CMD [ "python", "app.py" ]
