FROM python:3.6.10
COPY . /app
WORKDIR /app
RUN pip install -r ./src/requirements.txt
RUN python -m spacy download en_core_web_lg
EXPOSE 5000
CMD python ./src/RESTService.py