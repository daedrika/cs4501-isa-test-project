# Generated by Django 2.1 on 2018-11-14 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microservices', '0003_authenticator'),
    ]

    operations = [
        migrations.AddField(
            model_name='musician',
            name='email',
            field=models.CharField(default='person@site.com', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='musician',
            name='password',
            field=models.CharField(default='password', max_length=50),
            preserve_default=False,
        ),
    ]
