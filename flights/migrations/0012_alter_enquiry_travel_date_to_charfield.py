from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0011_alter_enquiry_label_colour_alter_enquiry_label_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='travel_date',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
    ]
