# Generated by Django 5.1.7 on 2025-06-29 17:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_listing_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="added_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="listing",
            name="image",
            field=models.CharField(
                default="https://static.vecteezy.com/system/resources/thumbnails/004/141/669/small/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg",
                max_length=200,
                null=True,
            ),
        ),
    ]
