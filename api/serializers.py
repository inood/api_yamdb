from rest_framework import serializers

from api.models import Category, Comment, Genre, Review, Title
from users.models import YamUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, attrs):
        if (self.context['request'].stream.method == 'POST'
                and Review.objects.filter(
                    author=self.context['request'].user,
                    title_id=self.context['view'].kwargs['title_id']
                    ).exists()):
            raise serializers.ValidationError('Такой отзыв уже существует!')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date',)


class GetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.SlugField()


class YamUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = YamUser
        fields = (
            "first_name", "last_name",
            "username", "bio", "email", "role")
