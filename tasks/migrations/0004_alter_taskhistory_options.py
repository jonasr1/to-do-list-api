# Generated by Django 5.1.4 on 2025-01-25 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_taskhistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskhistory',
            options={'ordering': ['-version']},
        ),
    ]
