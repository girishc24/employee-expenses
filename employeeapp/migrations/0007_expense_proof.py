# Generated by Django 5.0.4 on 2024-04-28 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeapp', '0006_alter_expense_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='proof',
            field=models.CharField(choices=[('TAX INVOICE', 'TAX INVOICE'), ('NOT APPLICABLE', 'NOT APPLICABLE'), ('VOUCHER ', 'VOUCHER'), ('RESPECTIVE BILL', 'RESPECTIVE BILL')], default='RESPECTIVE BILL', max_length=50),
        ),
    ]
