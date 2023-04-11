# Generated by Django 4.2 on 2023-04-11 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=20)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('like_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'post',
            },
        ),
    ]
