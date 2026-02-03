from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True,
                              verbose_name='Изображение',)
    tags = models.ManyToManyField(
        Tag, through='Scope', related_name='articles')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):
    # связь с моделью Article
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')

    # связь с моделью Tag
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')

    # метка о том, что раздел основной
    main_tag = models.BooleanField(default=False, verbose_name='Основной раздел')

    class Meta:
        # для того, чтобы один тег не мог быть связан со статьёй 2 раза
        unique_together = ['article', 'tag']

        verbose_name = 'Раздел статьи'
        verbose_name_plural = 'Разделы статьи'

        # сортировка, сначала основной тег, потом дополнительные по алфовитк
        ordering = ['-main_tag', 'tag__name']
