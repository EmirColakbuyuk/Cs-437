# Generated by Django 4.2.8 on 2024-01-11 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_alter_news_published_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="link",
            field=models.URLField(blank=True, null=True, unique=True),
        ),
    ]
