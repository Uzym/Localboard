up:
	docker-compose --env-file .env -f docker-compose.yml up --build

down:
	docker-compose down

migration:
	docker-compose run apidemon alembic revision --autogenerate -m "migration db"

container-stop:
	bash $(docker stop $(docker ps -a -q))

container-rm:
	bash $(docker container rm $(docker ps -a -q))

clean-rabbitports:
	bash $(sudo systemctl stop rabbitmq-server)
	bash $(sudo netstat -tunpl | grep 4369 | awk '{ split($7,a,"/"); print a[1] }' | xargs sudo kill -9)

destroy-images:
	bash $(docker images | awk '{print $3}' | xargs docker rmi)