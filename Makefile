up:
	docker-compose up

down:
	docker-compose down

migrate:
	docker-compose run --rm --entrypoint "python manage.py migrate" caderneta_digital

migrations:
	docker-compose run --rm --entrypoint "python manage.py makemigrations" caderneta_digital 

test:
	docker-compose run --no-deps --rm --entrypoint "python manage.py test" caderneta_digital 

bash:
	docker-compose exec caderneta_digital bash

debug:
	docker-compose run --service-ports caderneta_digital
	
lint:
	bash "./lint.sh"