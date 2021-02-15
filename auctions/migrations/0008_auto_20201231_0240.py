# Generated by Django 3.1.4 on 2020-12-31 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_commentslisting_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentslisting',
            name='comments',
        ),
        migrations.AddField(
            model_name='auctlisting',
            name='comments',
            field=models.CharField(default='no comments yet.', max_length=200),
        ),
    ]
