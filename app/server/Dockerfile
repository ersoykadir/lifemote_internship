FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT python main.py
EXPOSE 3000

# docker run -dp 0.0.0.0:3306:3306 \
#   --network todo-app \
#   -v item-mysql-data:/var/lib/mysql \
#   -e MYSQL_ROOT_PASSWORD=secret \
#   -e MYSQL_DATABASE=items \
#   mysql:8.0 

# docker run -dp 0.0.0.0:3000:3000 \
#   --network todo-app \
#   -e HOST=0.0.0.0 \
#   -e PORT=3000 \
#   -e MYSQL_HOST=0.0.0.0 \
#   -e MYSQL_USER=root \
#   -e MYSQL_PASSWORD=secret \
#   -e MYSQL_DB=items \
#   -e GOOGLE_CLIENT_ID=secret \
#   -e GOOGLE_CLIENT_SECRET=secret \
#   -e SECRET_KEY=secret \
#   trial:latest