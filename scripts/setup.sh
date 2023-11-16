sudo usermod -aG docker $USER
docker volume create auth-redis-data
docker volume create auth-mariadb-data
docker network create auth-network