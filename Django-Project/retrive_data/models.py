from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import json
import pandas as pd

class Shop(models.Model):
    serving = RichTextUploadingField(blank=True, null=True)
    place_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=60)
    work_time = models.CharField(max_length=255)
    locations = models.CharField(max_length=255)
    services = RichTextUploadingField(blank=True, null=True)
    serving_car_type = models.CharField(max_length=255)
    image_urls = models.JSONField(blank=True, null=True)
    long_lat = models.CharField(max_length=50)

    def clean(self):
        if self.image_urls:
            # Replace "NaN" with a valid JSON value (e.g., empty list [])
            self.image_urls = json.dumps([url if url != "NaN" else None for url in self.image_urls])
    def save(self, *args, **kwargs):
        # Convert the list to JSON before saving
        if self.image_urls:
            self.image_urls = json.dumps(self.image_urls)
        super().save(*args, **kwargs)        
    @classmethod
    def from_dataframe(cls, df):
        # Remove rows with NaN values
        df_cleaned = df.dropna()
        instances = []
        for index, row in df_cleaned.iterrows():
            shop = cls(
                serving=row['serving'],
                place_name=row['place_name'],
                phone_number=row['phone_number'],
                work_time=row['work_time'],
                locations=row['locations'],
                services=row['services'],
                serving_car_type=row['serving_car_type'],
                image_urls=json.dumps(row['image_urls']),
                long_lat=row['long_lat']
            )
            instances.append(shop)
        return instances

    def __str__(self):
        return self.place_name
