# Generated by Django 3.2.12 on 2022-02-15 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_temporaldata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tdsdata',
            name='end_position',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tdsdata',
            name='lockin_time',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tdsdata',
            name='start_position',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tdsdata',
            name='step',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
