from rest_framework import serializers

from .models import Note, Label

class NoteSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = ('id','name','body','labels',)


    def get_labels(self,obj):
        return obj.labels.all().values('id','name')


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id','name')
