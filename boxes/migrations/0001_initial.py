from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('internal_length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('internal_width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('internal_height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_weight_capacity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'box',
                'ordering': ['cost'],
            },
        ),
    ]