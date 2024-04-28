# Generated by Django 5.0.4 on 2024-04-27 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeapp', '0005_alter_expense_updated_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='payment',
            field=models.CharField(choices=[('UPI', 'UPI'), ('Cash', 'Cash'), ('Credit/Dedit', 'Credit/Dedit'), ('Net Banking', 'Net Banking')], default='UPI', max_length=50),
        ),
    ]
