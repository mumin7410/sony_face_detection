# Generated by Django 4.2.5 on 2024-02-04 11:54

from django.db import migrations, models
import face_recog.models


class Migration(migrations.Migration):
    dependencies = [
        ("face_recog", "0005_alter_transaction_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="Image",
            field=models.ImageField(upload_to=face_recog.models.image_upload_path),
        ),
    ]