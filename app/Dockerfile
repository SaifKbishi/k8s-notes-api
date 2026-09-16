FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
#CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5000", "--debug"]k8s-notes-api