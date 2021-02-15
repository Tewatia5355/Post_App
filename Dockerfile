FROM python:alpine3.7 
COPY ./Backend /app
WORKDIR /app
RUN pip install -r requirements.txt 
EXPOSE 8081
ENTRYPOINT [ "python3" ] 
CMD [ "api.py" ] 