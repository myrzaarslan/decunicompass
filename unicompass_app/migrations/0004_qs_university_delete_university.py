# Generated by Django 5.0.7 on 2024-08-01 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unicompass_app', '0003_the_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='QS_University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('overall_score', models.FloatField()),
                ('rank', models.PositiveIntegerField()),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='University',
        ),
    ]
