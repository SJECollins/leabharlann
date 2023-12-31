# Generated by Django 4.2.3 on 2023-08-18 15:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybookreview',
            name='rating',
            field=models.IntegerField(default=5, help_text='Enter your rating', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterUniqueTogether(
            name='mybookreview',
            unique_together={('user', 'book')},
        ),
    ]
