# Generated by Django 5.0.4 on 2024-04-13 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_variant_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='variant',
            unique_together=set(),
        ),
    ]
