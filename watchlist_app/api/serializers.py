from rest_framework import serializers
from watchlist_app.models import WatchList
from watchlist_app.models import StreamPlatform
from watchlist_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField()
    
    class Meta:
        model=Review
        exclude=('watchlist',)
        #fields="__all__"
    

class WatchListSerializer(serializers.ModelSerializer):
    len_title=serializers.SerializerMethodField()
    #reviews=ReviewSerializer(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name')
    class Meta:
        model=WatchList
        fields="__all__"
    
    def get_len_title(self, obj):
        return len(obj.title)
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist= WatchListSerializer(many=True, read_only=True)
    class Meta:
        model=StreamPlatform
        fields="__all__"
        
        
        

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         """
        
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Movie` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance