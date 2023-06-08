# Generated by Django 4.2.2 on 2023-06-08 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.CharField(choices=[('other', 'Other'), ('meat', 'Meat'), ('fruit', 'Fruit'), ('veggie', 'Veggie'), ('dry', 'Dry Seasoning/Powders'), ('wet', 'Liquids/Oils'), ('sauce', 'Sauce'), ('dairy', 'Dairy'), ('grain', 'Rice/Pasta'), ('product', 'Off-the-Shelf')], max_length=50),
        ),
    ]
