# Generated by Django 3.2.10 on 2023-08-19 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countries_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('capital', models.CharField(max_length=100)),
                ('area', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HousePricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.IntegerField()),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('housing_median', models.IntegerField()),
                ('total_rooms', models.IntegerField()),
                ('total_bedrooms', models.IntegerField()),
                ('population', models.IntegerField()),
                ('households', models.IntegerField()),
                ('median_income', models.DecimalField(decimal_places=5, max_digits=10)),
                ('ocean_proximity', models.CharField(max_length=100)),
                ('median_house_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NycData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BLKID', models.CharField(max_length=50)),
                ('POPN_TOTAL', models.IntegerField()),
                ('POPN_WHITE', models.IntegerField()),
                ('POPN_BLACK', models.IntegerField()),
                ('POPN_NATIV', models.IntegerField()),
                ('POPN_ASIAN', models.IntegerField()),
                ('POPN_OTHER', models.IntegerField()),
                ('BORONAME', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedSQLData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sql_file', models.FileField(upload_to='sql_data')),
                ('is_loaded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFileData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dbf_file', models.FileField(upload_to='Spatial_Files')),
                ('shp_file', models.FileField(upload_to='Spatial_Files')),
                ('shx_file', models.FileField(upload_to='Spatial_Files')),
                ('database_name', models.CharField(max_length=500)),
                ('is_loaded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Nyc_Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_coord', models.DecimalField(decimal_places=20, max_digits=30)),
                ('y_coord', models.DecimalField(decimal_places=20, max_digits=30)),
                ('nyc_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.nycdata')),
            ],
        ),
        migrations.CreateModel(
            name='Country_Coorinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.countries_info')),
            ],
        ),
    ]
