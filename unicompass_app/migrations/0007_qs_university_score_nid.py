# Generated by Django 5.0.7 on 2024-08-01 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unicompass_app', '0006_alter_qs_university_overall_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='qs_university',
            name='score_nid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
