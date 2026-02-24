# Generated migration for adding travel_date and notes fields to Enquiry model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='travel_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enquiry',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
