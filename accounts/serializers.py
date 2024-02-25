from rest_framework import serializers

from accounts.models import CustomUser
from speedolearn.settings import SIMPLE_JWT



class CustomUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "contact",
            "address",
            "name",
            "isAdmin",
        ]
        # fields = "__all__"

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name

class UserSerializerWithToken(serializers.ModelSerializer):
    token_lifetime = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser
        # fields = [""]
        # fields = ["token_lifetime"]
        fields = ["token_lifetime",]

    # def get_token(self, obj):
    #     token = RefreshToken.for_user(obj)
    #     return str(token.access_token)

    def get_token_lifetime(self, obj):
        token_lifetime = SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        return token_lifetime