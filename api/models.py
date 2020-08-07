from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pytils.translit import slugify

User = settings.AUTH_USER_MODEL


class BaseCatalog(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(verbose_name='SLUG', null=True,
                            blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Genre(BaseCatalog):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseCatalog):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год',
                               null=True,
                               blank=True,
                               db_index=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='titles')
    description = models.TextField(null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name} ({self.year}г.)'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        'Оценка от 1 до 10',
        null=False,
        default=5,
        validators=(
            MinValueValidator(1, message='Не меньше 1'),
            MaxValueValidator(10, message='Не больше 10')
        )
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Комментарий')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author} к {self.review}'
