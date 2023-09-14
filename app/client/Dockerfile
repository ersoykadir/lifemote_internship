FROM python:3.10-alpine
WORKDIR /app
# Layer for dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt
# Layer for source code
COPY . .
ENTRYPOINT ["python", "main.py"]
EXPOSE 5000

# docker build -t app-client:latest ./app/client

# docker run --name app-client-1 \
#     -dp 0.0.0.0:5000:5000 \
#     --network app_my-network \
#     -e SERVER_IP=0.0.0.0 \
#     -e SERVER_PORT=3000 \
#     app-client:latest