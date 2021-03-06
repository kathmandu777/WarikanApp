# Generated by Django 3.1.7 on 2021-03-21 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SplitingBills', '0006_auto_20210319_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='cost',
            field=models.PositiveSmallIntegerField(verbose_name='価格'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='meal_name',
            field=models.CharField(max_length=50, verbose_name='料理名'),
        ),
        migrations.AlterField(
            model_name='money',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SplitingBills.meal', verbose_name='どの食事についてか'),
        ),
    ]
