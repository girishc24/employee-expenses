# Generated by Django 5.0.4 on 2024-04-28 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeapp', '0007_expense_proof'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='document',
            field=models.FileField(default=0, upload_to='employeeapp/images'),
            preserve_default=False,
        ),
    ]