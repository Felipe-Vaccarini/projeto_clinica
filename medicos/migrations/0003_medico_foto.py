# Generated by Django 4.1.3 on 2022-12-05 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0002_medico_cpf_medico_endbairro_medico_endcep_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='foto',
            field=models.ImageField(default=0, upload_to='foto/'),
            preserve_default=False,
        ),
    ]