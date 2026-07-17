from .common import *

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()
    country_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'tagline',
            'profile_pic',
            'country',
            'country_name',
            'languages',
            'skills',
            'is_seller',
            'date_joined',
        ]
        
    def get_country_name(self, obj):
        return obj.country.name if obj.country else None


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic', 'first_name', 'last_name', 'date_joined']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = '__all__'


