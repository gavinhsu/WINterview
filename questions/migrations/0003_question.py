# Generated by Django 3.0.1 on 2020-03-21 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0002_delete_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.CharField(max_length=10000)),
                ('Field', models.CharField(max_length=100)),
                ('Ques', models.TextField(max_length=100)),
            ],
        ),
    ]
