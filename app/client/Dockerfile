FROM python:3.10-alpine
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
EXPOSE 5000

# docker run -dp 0.0.0.0:5000:5000 \
#   --network app_my-network \
#   -e SERVER_IP=0.0.0.0 \
#   -e SERVER_PORT=3000 \
#   trial:latest
# docker run --name app-client-1 \
#     -p 0.0.0.0:5000:5000 \
#     --network app_my-network \
#     -e SERVER_IP=0.0.0.0 \
#     -e SERVER_PORT=3000 \
#     app-client:latest