from django.db import migrations
from pgvector import django as pgvector_django


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [pgvector_django.VectorExtension()]
