import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.image.url)
        )
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    pokemon_wrapper = {}
    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    pokemon_wrapper['title_ru'] = pokemon.title_ru
    pokemon_wrapper['title_en'] = pokemon.title_en
    pokemon_wrapper['title_jp'] = pokemon.title_jp
    pokemon_wrapper['description'] = pokemon.description
    pokemon_wrapper['img_url'] = pokemon.image.url
    if pokemon.previous_evolution:
        pokemon_wrapper['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title_ru,
            'img_url': pokemon.previous_evolution.image.url
        }
    if pokemon.next_evolution.first():
        pokemon_wrapper['next_evolution'] = {
            'pokemon_id': pokemon.next_evolution.first().id,
            'title_ru': pokemon.next_evolution.first().title_ru,
            'img_url': pokemon.next_evolution.first().image.url
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon.pokemon_entities.all():
        add_pokemon(
            folium_map,  entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.image.url)
        )
    return render(request, 'pokemon.html', context={
                'map': folium_map._repr_html_(), 'pokemon': pokemon_wrapper
            })
