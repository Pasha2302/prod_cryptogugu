# Generated by Django 5.1.5 on 2025-02-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auditinfo_coindescription_coinsocials_presaleinfo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, related_name='coin', to='app.label'),
        ),
    ]
