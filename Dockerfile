FROM python.3.14-alpine

RUN mkdir /mimasapp
WORKDIR /mimasapp
COPY /mimasapp .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
