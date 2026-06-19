from djoser.serializers import UserCreateSerializer as BaseUserCreateSerialiser,UserSerializer as BaseUserSerialiser
class UserCreateSerializer(BaseUserCreateSerialiser):
    class Meta(BaseUserCreateSerialiser.Meta):
        fields=['id','first_name','last_name','email','password','address','phone_number']



class UserSerializer(BaseUserSerialiser):
    class Meta(BaseUserSerialiser.Meta):
        ref_name='CustomUser'

        fields=['id','first_name','last_name','address','email','phone_number']

