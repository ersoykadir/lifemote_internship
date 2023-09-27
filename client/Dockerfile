FROM python:3.10-alpine
WORKDIR /app
# Layer for dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt
# Add bash
RUN apk add --no-cache bash
# Layer for source code
COPY . .
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]

# docker build -t lifemote_internship-client:latest ./client

# docker run --name lifemote_internship-client-1 \
#     -dp 5000:5000 \
#     --network=lifemote_internship_container_network \
#     -e ACCESS_TOKEN_SECRET=secret \
#     -e SERVER_HOST=server \
#     -e SERVER_PORT=3000 \
#     -e TEST_CASE=1 \
#     lifemote_internship-client:latest