# Generated by Django 2.2.1 on 2019-06-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expressions', '0002_auto_20190606_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expression',
            name='result',
            field=models.IntegerField(null=True),
        ),
    ]
