# Generated by Django 2.2.3 on 2019-08-16 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0004_año_enero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='año',
            name='enero',
            field=models.CharField(default='0000 0000 0000 0000 0000', max_length=155),
        ),
    ]
