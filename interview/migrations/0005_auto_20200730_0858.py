# Generated by Django 3.0.7 on 2020-07-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0004_interview_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(max_length=5000),
        ),
    ]
