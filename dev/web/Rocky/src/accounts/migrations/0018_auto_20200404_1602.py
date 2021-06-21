# Generated by Django 2.2.7 on 2020-04-04 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20200403_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tollbillings',
            name='tollgate_in',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_toll_bill', to='tollgate.TollgateLogs'),
        ),
        migrations.AlterField(
            model_name='tollbillings',
            name='tollgate_out',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='out_toll_bill', to='tollgate.TollgateLogs'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='wallet_balance',
            field=models.IntegerField(default=0),
        ),
    ]