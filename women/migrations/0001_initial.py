# Generated by Django 4.0.3 on 2022-03-27 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Category')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Photo')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time Create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Time Update')),
                ('is_published', models.BooleanField(default=True, verbose_name='Is Published')),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='women.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Famous women',
                'verbose_name_plural': 'Famous women',
                'ordering': ['time_create', 'title'],
            },
        ),
    ]
