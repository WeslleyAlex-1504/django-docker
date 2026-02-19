#!/usr/bin/env python
import os
import sys
import django

# Add the apps directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.core.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created successfully.")
else:
    print("Superuser 'admin' already exists.")

print("Admin credentials:")
print("Username: admin")
print("Password: admin123")
print("Email: admin@example.com")