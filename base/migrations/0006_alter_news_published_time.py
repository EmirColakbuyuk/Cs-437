# Generated by Django 4.2.8 on 2024-01-11 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_alter_news_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="published_time",
            field=models.TextField(blank=True, null=True),
        ),
    ]
