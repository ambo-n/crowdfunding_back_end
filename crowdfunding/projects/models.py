from django.db import models
from django.contrib.auth import get_user_model
import requests
from django.conf import settings
from django.core.exceptions import ValidationError
import os

class Category(models.Model):
    description = models.CharField(max_length=200)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True)
    suburb = models.CharField(max_length=100)
    postcode = models.IntegerField()
    country = models.CharField(max_length=60, default='Australia')

    AUSTRALIAN_CAPITAL_TERRIORY = "ACT"
    NEW_SOUTH_WALES = "NSW"
    NORTHERN_TERROTIRY = "NT"
    QUEENSLAND = "QLD"
    SOUTH_AUSTRALIA = "SA"
    TASMANIA = "TAS"
    VICTORIA = "VIC"
    WESTERN_AUSTRALIA = "WA"

    STATES_CHOICES ={
        AUSTRALIAN_CAPITAL_TERRIORY: "ACT",
        NEW_SOUTH_WALES: "NSW",
        NORTHERN_TERROTIRY: "NT",
        QUEENSLAND: "QLD",
        SOUTH_AUSTRALIA: "SA",
        TASMANIA: "TAS",
        VICTORIA: "VIC",
        WESTERN_AUSTRALIA: "WA",}
    
    state = models.CharField(
        max_length=3,
        choices = STATES_CHOICES,
        default=WESTERN_AUSTRALIA)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0)

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects')
    
    category = models.ManyToManyField(Category, related_name='projects')

    def save(self, **kwargs):

        address = f"{self.address},{self.suburb}, {self.state}, {self.postcode}, {self.country}"
        api_key = settings.GOOGLE_API_KEY
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}")
        
        if response.status_code == 200:
            api_response_dict = response.json()
            
            if api_response_dict.get('status') == 'OK':
                self.latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                self.longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        
        super().save(**kwargs)

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='pledges')
    support = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges',
    )



