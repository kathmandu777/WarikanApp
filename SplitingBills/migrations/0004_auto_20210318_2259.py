# Generated by Django 3.1.7 on 2021-03-18 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SplitingBills', '0003_auto_20210318_2252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='day',
            old_name='x',
            new_name='usedfood',
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('joined', models.ManyToManyField(to='SplitingBills.Day')),
            ],
        ),
    ]
