# Generated by Django 4.2.9 on 2024-03-02 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0004_alter_cart_pid_alter_cart_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]