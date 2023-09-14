FROM python:3.10
WORKDIR /app
# Layer for dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt
# Layer for source code
COPY . .
ENTRYPOINT ["sh", "-c", "alembic upgrade head && python main.py"]
EXPOSE 3000

# docker build -t app-server:latest ./app/server

# docker run --name app-mysql-1 \
#     -dp 0.0.0.0:3306:3306 \
#     --network app_my-network --network-alias mysql\
#     -v todo-mysql-data:/var/lib/mysql \
#     -e MYSQL_ROOT_PASSWORD=secret \
#     -e MYSQL_DATABASE=items \
#     mysql:8.0

# docker run --name app-server-1 \
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
#   -e SECRET_KEY=d29dc10453b57bdf4d05e183d81b3074a5f56f2ef4c636aa52fb0472ec6fceb3 \
#   app-server:latest