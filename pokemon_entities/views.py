import folium
import json

from django.http import HttpResponseNotFound, request
from django.shortcuts import render
from .models import PokemonEntity


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
    pokemons = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons:
            add_pokemon(
                folium_map, pokemon.lat,
                pokemon.lon,
                request.build_absolute_uri(pokemon.pokemon.image.url)
            )

    pokemons_on_page = []

    for pokemon in pokemons:
        if pokemon.pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.pokemon.image.url),
                'title_ru': pokemon.pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_entities = PokemonEntity.objects.filter(pokemon__id=pokemon_id)
    print()
    pokemon = {}
    if not pokemon_entities:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    else:
        pokemon_obj = PokemonEntity.objects.filter(pokemon__id=pokemon_id).first().pokemon
        pokemon['title_ru'] = pokemon_obj.title
        pokemon['img_url'] = pokemon_obj.image.url
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
