#!/bin/bash

# default superuser
# cpf: 78223564025
# email: 'admin@example.com'
# password: 'admin'

echo "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not len(User.objects.all()):
    User.objects.create_superuser('admin', cpf=78223564025, email='admin@example.com', dataNascimento='2000-01-01', password='admin')" | python manage.py shell