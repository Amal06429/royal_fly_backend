# Generated migration for adding created_by field to Enquiry model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_enquiry_travel_date_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='created_by',
            field=models.CharField(
                choices=[('customer', 'Customer'), ('admin', 'Admin')],
                default='customer',
                max_length=10
            ),
        ),
    ]
