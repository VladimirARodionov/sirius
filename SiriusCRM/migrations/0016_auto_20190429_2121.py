# Generated by Django 2.1.7 on 2019-04-29 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SiriusCRM', '0015_auto_20190425_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadcomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_value', to='SiriusCRM.CrmComment'),
        ),
        migrations.AlterField(
            model_name='leadcomment',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_value', to='SiriusCRM.Lead'),
        ),
    ]
