# Generated by Django 4.1.2 on 2022-10-22 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_alter_person_options_alter_person_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fruit",
            fields=[
                (
                    "name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("price", models.IntegerField(blank=True)),
            ],
            options={
                "verbose_name": "fruit",
                "verbose_name_plural": "fruits",
                "db_table": "fruit",
            },
        ),
    ]
