# Generated by Django 2.1.8 on 2020-03-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_urls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urls',
            name='url_link',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]