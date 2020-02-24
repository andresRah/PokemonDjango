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

def getAndSavePokemonChainID(request):
    try:
        chain_id = request.GET['chainID']
        utilities_pokemon = utilities.UtilitiesPokemon()
        response_utility = utilities_pokemon.searchChainByID(chain_id)
        status = response_utility[0]

        if status:
            response = {'status': "Register created....",
                        'data': json.loads(response_utility[1])}
        else:
            response = "Register already exists"
    except Exception as ex:
        response = str(ex)
    return HttpResponse(json.dumps(response), content_type='aplication/json')