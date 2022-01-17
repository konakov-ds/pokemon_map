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
        if pokemon.image:
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
    pokemon_entities = PokemonEntity.objects.filter(pokemon__id=pokemon_id)
    pokemon = {}
    if not pokemon_entities:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    else:
        pokemon_obj = pokemon_entities.first().pokemon
        pokemon['title_ru'] = pokemon_obj.title_ru
        pokemon['title_en'] = pokemon_obj.title_en
        pokemon['title_jp'] = pokemon_obj.title_jp
        pokemon['description'] = pokemon_obj.description
        pokemon['img_url'] = pokemon_obj.image.url
        if pokemon_obj.previous_evolution:
            pokemon['previous_evolution'] = {
                'pokemon_id': pokemon_obj.previous_evolution.id,
                'title_ru': pokemon_obj.previous_evolution.title_ru,
                'img_url': pokemon_obj.previous_evolution.image.url
            }
        if pokemon_obj.next_evolution.first():
            pokemon['next_evolution'] = {
                'pokemon_id': pokemon_obj.next_evolution.first().id,
                'title_ru': pokemon_obj.next_evolution.first().title_ru,
                'img_url': pokemon_obj.next_evolution.first().image.url
            }

        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
        for entity in pokemon_entities:
                add_pokemon(
                    folium_map,  entity.lat,
                    entity.lon,
                    request.build_absolute_uri(entity.pokemon.image.url)
                )
        return render(request, 'pokemon.html', context={
                    'map': folium_map._repr_html_(), 'pokemon': pokemon
                })
