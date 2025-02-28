all: build

build: 
	docker compose up --build -d

status: 
	docker compose -f docker-compose.yml ps

check:
	docker compose exec postgres psql -U tsuchen -d piscineds -h localhost -W

stop: 
	docker compose -f docker-compose.yml stop

start: 
	docker compose -f docker-compose.yml start

down: 
	docker compose -f docker-compose.yml down

clean: 
	docker compose -f docker-compose.yml down -v --remove-orphans

re: clean all

.PHONY: all build status stop start down clean re