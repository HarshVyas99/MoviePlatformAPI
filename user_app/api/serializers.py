from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'inputtype': 'password'},write_only=True)
    
    class Meta:
        model=User
        fields=['username', 'email', 'password','password2']
        extra_kwargs={
            'password': {'write_only': True},
        }
        
    
    def save(self):
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        email=self.validated_data['email']
        
        
        
        if password!=password2:
            raise serializers.ValidationError({'error':'Password mismatch'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'Email already exists'})
        
        account= User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account
        
        