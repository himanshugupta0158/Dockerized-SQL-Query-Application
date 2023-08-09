# Generated by Django 4.2.4 on 2023-08-08 11:29

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_uploadfiledata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploadfiledata",
            name="dbf_file",
            field=models.FileField(upload_to=app.models.RandomFolder_Name),
        ),
        migrations.AlterField(
            model_name="uploadfiledata",
            name="shp_file",
            field=models.FileField(upload_to=app.models.RandomFolder_Name),
        ),
        migrations.AlterField(
            model_name="uploadfiledata",
            name="shx_file",
            field=models.FileField(upload_to=app.models.RandomFolder_Name),
        ),
    ]
