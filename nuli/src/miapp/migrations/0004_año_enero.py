# Generated by Django 2.2.3 on 2019-08-16 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0003_año_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='año',
            name='enero',
            field=models.CharField(default='00000000000000000000', max_length=124),
        ),
    ]
