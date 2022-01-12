from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Название, рус.')
    title_en = models.CharField(max_length=200, default=None, blank=True, null=True, verbose_name='Название, англ.')
    title_jp = models.CharField(max_length=200, default=None, blank=True, null=True, verbose_name='Название, япон.')
    description = models.TextField(default=None, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='pokemons_img', blank=True, null=True, verbose_name='Изображение')
    previous_evolution = models.ForeignKey(
        "self",
        related_name='previous_evolutions',
        on_delete=models.SET('Неизвестно'),
        default=None,
        null=True,
        blank=True,
        verbose_name='Из кого эволюционирует'
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=1, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(default=None, blank=True, null=True, verbose_name='Когда появится')
    disappeared_at = models.DateTimeField(default=None, blank=True, null=True, verbose_name='Когда исчезнет')
    level = models.IntegerField(default=None, blank=True, null=True, verbose_name='Уровень')
    health = models.IntegerField(default=None, blank=True, null=True, verbose_name='Очки жизни')
    strength = models.IntegerField(default=None, blank=True, null=True, verbose_name='Очки силы')
    defense = models.IntegerField(default=None, blank=True, null=True, verbose_name='Очки защиты')
    stamina = models.IntegerField(default=None, blank=True, null=True, verbose_name='Очки выносливости')
