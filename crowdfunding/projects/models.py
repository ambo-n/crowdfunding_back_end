from django.db import models
from django.contrib.auth import get_user_model

class Location(models.Model):
    address = models.TextField()
    suburb = models.CharField(max_length=100)
    postcode = models.IntegerField()
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
        default=WESTERN_AUSTRALIA
    )
class Category(models.Model):
    description = models.CharField(max_length=200)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='projects')

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



