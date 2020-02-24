from django.http import HttpResponse
import json
from pokemon import utilities

# Create your views here.


def searchPokemonInfoByName(request):
    try:
        name = request.GET['name']

        if len(name) < 4:
            response = "The minimum character allowed is 4"
        else:
            utilities_pokemon = utilities.UtilitiesPokemon()
            pokemon_list = utilities_pokemon.getPokemonEvolutionByName(name)

            if len(pokemon_list) > 0:
                response = pokemon_list
            else:
                response = "Not pokemon found"
    except Exception as ex:
        response = str(ex)

    return HttpResponse(json.dumps(response), content_type='aplication/json')