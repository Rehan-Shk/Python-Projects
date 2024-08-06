# Generated by Django 4.2.14 on 2024-07-29 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitems',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='LittleLemonAPI.category'),
        ),
    ]
