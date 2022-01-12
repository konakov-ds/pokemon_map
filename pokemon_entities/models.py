from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default=None, blank=True, null=True)
    title_jp = models.CharField(max_length=200, default=None, blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True)
    image = models.ImageField(upload_to='pokemons_img', blank=True, null=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET('Неизвестно'),
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=1)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=None)
    disappeared_at = models.DateTimeField(default=None)
    level = models.IntegerField(default=None)
    health = models.IntegerField(default=None)
    strength = models.IntegerField(default=None)
    defense = models.IntegerField(default=None)
    stamina = models.IntegerField(default=None)
