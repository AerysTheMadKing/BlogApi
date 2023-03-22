from rest_framework import serializers

from comment.models import Comments


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comments
        fields = '__all__'


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'body', 'post', 'created_at')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post_title'] = instance.post.title
        return repr