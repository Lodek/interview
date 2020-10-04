# Generated by Django 3.0.7 on 2020-08-17 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0006_auto_20200816_2208'),
        ('base', '0003_auto_20200816_2208'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Band',
        ),
        migrations.AddField(
            model_name='position',
            name='seniority',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='positions', to='base.Seniority'),
            preserve_default=False,
        ),
    ]