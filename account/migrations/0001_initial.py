# Generated by Django 4.2 on 2023-05-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('joinedDate', models.DateField(max_length=50)),
                ('role', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
