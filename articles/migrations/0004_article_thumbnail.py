# Generated by Django 5.1.6 on 2025-02-14 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_remove_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
