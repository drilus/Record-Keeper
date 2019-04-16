from rest_framework import serializers
from keeperapp.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    profile_avatar = serializers.SerializerMethodField()

    def get_avatar(self, restaurant):
        request = self.context.get('request')
        avatar_url = Profile.avatar.url
        return request.build_absolute_uri(avatar_url)

    class Meta:
        model = Profile
        fields = ('id', 'phone', 'address', 'city', 'state', 'zip', 'avatar')
