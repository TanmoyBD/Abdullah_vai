# Generated by Django 4.2.7 on 2023-11-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='forgotten_token',
            field=models.CharField(blank=True, default='', max_length=36, null=True),
        ),
    ]
