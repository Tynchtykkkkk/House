from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(null=True, unique=True)
    password = models.CharField(max_length=255)
    RoleChoices = (
        ('seller', 'seller'),
        ('buyer', 'buyer'),
    )
    role = models.CharField(max_length=20, choices=RoleChoices, default='seller')
    registered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Property(models.Model):
    property_name = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    property_stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    price = models.PositiveIntegerField()
    PropertyTypeChoices = (
        ('Квартиру', 'Квартиру'),
        ('Дом', 'Дом'),
        ('Участок', 'Участок'),
        ('Дачу', 'Дачу'),
        ('Гараж', 'Гараж'),
    )
    property_type = models.CharField(max_length=20, choices=PropertyTypeChoices)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.property_name}'

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images')

    def __str__(self):
        return f'{self.property}, {self.image}'

class Region(models.Model):
    region_name = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.region_name}'

class City(models.Model):
    city_name = models.CharField(max_length=55)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city_name}'

class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.district_name}'

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    room_number = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    RoomStatusChoices = (
    ('Занят', 'Занят'),
    ('Забронировано', 'Забронировано'),
    ('Свободен', 'Свободен'))
    room_status = models.CharField(max_length=30, choices=RoomStatusChoices)
    description = models.TextField()

    def __str__(self):
        return f'{self.property}, {self.room_number}'

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_image = models.ImageField(upload_to='room_images')

    def __str__(self):
        return f'{self.room}, {self.room_image}'

class Review(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    comment = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer}'