from .models import City, Room, Property, Review, Region
from modeltranslation.translator import TranslationOptions, register


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('property_name', 'description',)


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region_name',)