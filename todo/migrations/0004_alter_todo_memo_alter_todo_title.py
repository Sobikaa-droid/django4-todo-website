# Generated by Django 4.0.6 on 2022-08-18 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todo_memo_alter_todo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='memo',
            field=models.TextField(blank=True, max_length=3000),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]