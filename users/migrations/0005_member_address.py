# Generated by Django 3.0.4 on 2020-07-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_member_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='Address',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
