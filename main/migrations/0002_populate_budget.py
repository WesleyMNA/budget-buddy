from django.db import migrations


def populate_table(apps, schema_editor):
    table = apps.get_model('main', 'Budget')
    my_data_dict = {
        'Fixed',
        'Goal',
        'Investment',
        'Knowledge',
        'Pleasures',
    }

    for value in my_data_dict:
        table.objects.create(category=value)


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_table),
    ]
