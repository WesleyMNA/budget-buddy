from django.db import migrations


def populate_table(apps, schema_editor):
    table = apps.get_model('main', 'Category')
    my_data_dict = {
        'F',
        'G',
        'I',
        'K',
        'P',
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
