prod:
    docker-compose -f docker-compose.prod.yml up -d --build

down:
    docker-compose down