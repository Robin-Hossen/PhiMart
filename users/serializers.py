from djoser.serializers import UserCreateSerializer as BaseUserCreateSerialiser
class UserCreateSerializer(BaseUserCreateSerialiser):
    class Meta(BaseUserCreateSerialiser.Meta):
        fields=['id','first_name','last_name','email','password','address','phone_number']
