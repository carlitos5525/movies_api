from rest_framework import serializers
from watchlist_app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = "__all__"

    def get_len_name(self, object):
        length = len(object.name)
        return length

    #  object-level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Title and description should be different!")
        else:
            return data
    
    # field-level validation
    def validate_description(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        else:
            return value

# def name_lenght(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_lenght])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#        instance.name = validated_data.get('name', instance.name)
#        instance.description = validated_data.get('description', instance.description)
#        instance.active = validated_data.get('active', instance.active)
#        instance.save()
#        return instance

#     #object-level validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description should be different!")
#         else:
#             return data
    
#     # #field-level validation
#     def validate_description(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value
