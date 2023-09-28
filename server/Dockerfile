FROM python:3.10
WORKDIR /app
# Layer for dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt
# Layer for source code
COPY . .
# Layer for packaging
RUN pip install -e . 
EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]

# docker build -t lifemote_internship-server:latest ./server

# docker run --name lifemote_internship-mysql-1 \
#     -dp 0.0.0.0:3306:3306 \
#     --network app_my-network --network-alias mysql\
#     -v todo-mysql-data:/var/lib/mysql \
#     -e MYSQL_ROOT_PASSWORD=secret \
#     -e MYSQL_DATABASE=items \
#     mysql:8.0

# docker run --name lifemote_internship-server-1 \
#   -dp 0.0.0.0:3000:3000 \
#   --network app_my-network --network-alias server \
#   -e HOST=0.0.0.0 \
#   -e PORT=3000 \
#   -e MYSQL_HOST=mysql \
#   -e MYSQL_USER=root \
#   -e MYSQL_PASSWORD=secret \
#   -e MYSQL_DB=items \
#   -e GOOGLE_CLIENT_ID=secret \
#   -e GOOGLE_CLIENT_SECRET=secret \
#   -e SECRET_KEY=secret \
#   app-server:latest