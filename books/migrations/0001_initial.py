# Generated by Django 4.2.3 on 2023-08-09 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('honorific', models.CharField(blank=True, help_text="Enter the author's honorific (e.g. Mr, Mrs, Ms, Dr, etc.)", max_length=10)),
                ('first_name', models.CharField(blank=True, help_text="Enter the author's first name", max_length=100)),
                ('middle_name', models.CharField(blank=True, help_text="Enter the author's middle name", max_length=100)),
                ('last_name', models.CharField(blank=True, help_text="Enter the author's last name", max_length=100)),
                ('name', models.CharField(blank=True, help_text="Enter the author's name as it should be displayed", max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('number_shelves', models.PositiveIntegerField(default=0)),
                ('number_reads', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a book genre (e.g. Science Fiction, Fantasy, etc.)', max_length=100)),
                ('number_shelves', models.PositiveIntegerField(default=0)),
                ('number_reads', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Enter the book's title", max_length=140)),
                ('book_cover', models.ImageField(blank=True, help_text='Optional. Upload a book cover image', upload_to='book_covers')),
                ('number_shelves', models.PositiveIntegerField(default=0)),
                ('number_reads', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(help_text="Select the book's author", on_delete=django.db.models.deletion.CASCADE, to='books.author')),
                ('genre', models.ManyToManyField(help_text='Select at least one genre for this book', to='books.genre')),
            ],
        ),
    ]
