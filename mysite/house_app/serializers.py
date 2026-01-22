from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Property, PropertyImage, Review, City, Region, District, Room, RoomImage


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'phone_number', 'email', 'first_name', 'last_name', 'role')


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('id', 'image')


class ReviewSerializer(serializers.ModelSerializer):
    buyer = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'buyer', 'rating', 'comment', 'created_date')


class CitySerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = ['id', 'city_name', 'region']


class PropertyListSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    property_images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ('id', 'property_name', 'title', 'description', 'property_type',
                  'price', 'property_stars', 'city', 'property_images')


class PropertyDetailSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    property_images = PropertyImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    owner = UserProfileSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ('id', 'property_name', 'title', 'description', 'property_type',
                  'price', 'property_stars', 'is_active', 'city',
                  'owner', 'property_images', 'reviews')


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('property_name', 'title', 'description', 'property_type', 'price', 'property_stars', 'city')


class DistrictSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = District
        fields = ('id', 'district_name', 'city')


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ('id', 'room_image')


class RoomSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'room_number', 'price', 'room_status', 'description', 'property', 'room_images')