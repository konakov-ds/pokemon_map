from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200,
        verbose_name='Название, рус.'
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название, англ.'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название, япон.'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='pokemons_img',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    previous_evolution = models.ForeignKey(
        "self",
        related_name='next_evolution',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Из кого эволюционирует'
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities',
    )
    lat = models.FloatField(
        verbose_name='Широта'
    )
    lon = models.FloatField(
        verbose_name='Долгота'
    )
    appeared_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Когда появится'
    )
    disappeared_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Когда исчезнет'
    )
    level = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Очки жизни'
    )
    strength = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Очки силы'
    )
    defense = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Очки защиты'
    )
    stamina = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Очки выносливости'
    )
