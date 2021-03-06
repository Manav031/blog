# Generated by Django 3.2.13 on 2022-05-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_alter_blog_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(blank=True, choices=[('Approve', 'Approve'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=100, null=True),
        ),
    ]
