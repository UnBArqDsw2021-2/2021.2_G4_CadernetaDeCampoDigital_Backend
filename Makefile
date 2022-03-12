up:
	docker-compose up

down:
	docker-compose down

migrate:
	docker exec -it caderneta_digital_backend python manage.py migrate

migrations:
	docker exec -it caderneta_digital_backend python manage.py makemigrations

test:
	docker-compose run --no-deps --rm --entrypoint "python manage.py test" caderneta_digital 

bash:
	docker-compose exec caderneta_digital bash

lint:
	bash "./scripts/lint.sh"