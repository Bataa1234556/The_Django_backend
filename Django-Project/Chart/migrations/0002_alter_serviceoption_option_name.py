# Generated by Django 5.0.6 on 2024-05-27 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceoption',
            name='option_name',
            field=models.CharField(choices=[('Diagnose', 'Diagnose'), ('Oil', 'Oil Change'), ('Engine', 'Engine Repair'), ('Aggregate', 'Internal Car Repair'), ('Car-Battery', 'Battery Change'), ('Parts_of_Car', 'Movable Car Parts'), ('Air_condition', 'Air Conditioning'), ('Com-Diagnose', 'Computer Diagnosis'), ('Tire', 'Tire Services'), ('Kuzov', 'Car Appearance'), ('Brake', 'Brake Services'), ('Wash', 'Car Washing'), ('parts-selling', 'Parts Selling'), ('Car-Trade', 'Car Trading'), ('Car paint', 'Car Painting'), ('Fuel', 'Fuel'), ('Call-repair', 'Repair by Call'), ('Car loading', 'Car Transport')], max_length=100),
        ),
    ]
