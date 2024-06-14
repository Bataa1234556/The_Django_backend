from django.db import models
from data_models.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ServiceOption(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    OPTION_CHOICES = [
        ('Diagnose', 'Diagnose'),
        ('Oil', 'Oil Change'),
        ('Engine', 'Engine Repair'),
        ('Aggregate', 'Internal Car Repair'),
        ('Car-Battery', 'Battery Change'),
        ('Parts_of_Car', 'Movable Car Parts'),
        ('Air_condition', 'Air Conditioning'),
        ('Com-Diagnose', 'Computer Diagnosis'),
        ('Tire', 'Tire Services'),
        ('Kuzov', "Car Appearance"),
        ('Brake', 'Brake Services'),
        ('Wash', 'Car Washing'),
        ('parts-selling', 'Parts Selling'),
        ('Car-Trade', 'Car Trading'),
        ('Car paint', 'Car Painting'),
        ('Fuel', 'Fuel'),
        ('Call-repair', 'Repair by Call'),
        ('Car loading', 'Car Transport')
    ]
    option_name = models.CharField(max_length=100, choices=OPTION_CHOICES)
    option_description = models.TextField()
    icon = models.ImageField(upload_to='service_icons/')

    def __str__(self):
        return dict(self.OPTION_CHOICES).get(self.option_name, self.option_name)

class CostDiagram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_option = models.ForeignKey(ServiceOption, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_taken = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.service_option} - {self.date_taken}"


