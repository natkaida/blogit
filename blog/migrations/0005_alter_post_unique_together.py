# Generated by Django 4.1.7 on 2023-04-06 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_interest_unique_together'),
        ('blog', '0004_alter_comment_options_alter_post_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('owner', 'slug'), ('owner', 'title')},
        ),
    ]
