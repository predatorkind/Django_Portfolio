# Generated by Django 4.2.5 on 2023-09-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_employment_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=40)),
                ('url', models.CharField(max_length=300)),
            ],
        ),
    ]
