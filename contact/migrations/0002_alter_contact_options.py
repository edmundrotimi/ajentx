# Generated by Django 3.2.9 on 2021-11-07 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-date_created'], 'verbose_name': 'Contact Messages', 'verbose_name_plural': 'Contact Messages'},
        ),
    ]
