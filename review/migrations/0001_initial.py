# Generated by Django 4.2.3 on 2023-08-09 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyBookReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, help_text='Enter your review', max_length=500)),
                ('rating', models.PositiveIntegerField(default=3, help_text='Enter your rating')),
                ('private', models.BooleanField(default=True, help_text='Make review invisible to others')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('book', models.ForeignKey(help_text='Select the book', on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
