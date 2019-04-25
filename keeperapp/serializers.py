from rest_framework import serializers
from keeperapp.models import Profile, Record, Category


class ProfileSerializer(serializers.ModelSerializer):
    profile_avatar = serializers.SerializerMethodField()

    def get_avatar(self, restaurant):
        request = self.context.get('request')
        avatar_url = Profile.avatar.url
        return request.build_absolute_uri(avatar_url)

    class Meta:
        model = Profile
        fields = ('id', 'phone', 'address', 'city', 'state', 'zip', 'avatar')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'columns', 'options')


class RecordSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    def get_file(self, record):
        request = self.context.get('request')
        file_url = record.file.url
        return request.build_absolute_uri(file_url)

    class Meta:
        model = Record
        fields = ('category', 'data', 'file')
