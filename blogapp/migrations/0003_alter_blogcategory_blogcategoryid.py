# Generated by Django 3.2.13 on 2022-05-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_auto_20220505_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='blogcategoryid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]