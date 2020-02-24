from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
import json
import requests
from pokemon import models
# Create your views here.
post = [
    {
        'name': 'MontBlanc',
        'user': 'Andres Arevalo',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://d500.epimg.net/cincodias/imagenes/2019/08/14/motor/1565771492_166386_1565771651_noticia_normal.jpg'
    },
    {
        'name': 'MontBlanc',
        'user': 'Andres Arevalo',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://d500.epimg.net/cincodias/imagenes/2019/08/14/motor/1565771492_166386_1565771651_noticia_normal.jpg'
    },
    {
        'name': 'MontBlanc',
        'user': 'Andres Arevalo',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://d500.epimg.net/cincodias/imagenes/2019/08/14/motor/1565771492_166386_1565771651_noticia_normal.jpg'
    }
]

posts = [
    {
        'title': 'Mont Blanc',
        'user': {
            'name': 'Yésica Cortés',
            'picture': 'https://picsum.photos/60/60/?image=1027'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/800/600?image=1036',
    },
    {
        'title': 'Via Láctea',
        'user': {
            'name': 'Andres Leonardo Arevalo',
            'picture': 'https://picsum.photos/60/60/?image=1005'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/800/800/?image=903',
    },
    {
        'title': 'Nuevo auditorio',
        'user': {
            'name': 'Camilo Barrera',
            'picture': 'https://picsum.photos/60/60/?image=883'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/500/700/?image=1076',
    }
]

def list_pokemon(request):
    return render(request, 'feed.html', {'posts' : posts})

def list_pokemon1(request):
    """List existings pokemons"""
    content = []
    for p in post:
        content.append("""
             <p><strong>{name}</strong></p>
             <p><small>{user} - <i>{timestamp}</i></small></p>
             <figure><img src="{picture}"/></figure>
        """.format(**p))
    return HttpResponse('<br>'.join(content))

# Create your views here.
urlApi = 'https://pokeapi.co/api/v2/evolution-chain/%s'

def searchChainByID(request):
    idChain = 5
    for num in range(idChain):
        response = requests.get(urlApi % str(num+1))
        chains = response.json()
        evoData = chains['chain']
        evolutionId = chains['id']

        evoChain = getAllEvolutions(evoData, evolutionId)

        for pokemon in evoChain:
            info_specie = get_SpecieInfo(pokemon['url_specie'])
            pokemon.update(info_specie)

        evoChain = getEvolution_chain(evoChain)

        evoChain = cleanRespose(evoChain)

        pokemon_model = models.Pokemon()
        pokemon_model.savePokemon(evoChain)

    return HttpResponse(json.dumps(evoChain), content_type='application/json')

def cleanRespose(evoChain):
    listPokemon = []
    for pokemon in evoChain:
        listPokemonEvolution = []
        for evolution in pokemon['evolutions']:
            newDictionaryEvolution = {
                'id': evolution['id'],
                'evolutionChainId': evolution['evolutionChainId'],
                'name': evolution['name']
            }
            listPokemonEvolution.append(newDictionaryEvolution)

        newDictionary = {
            'name': pokemon['name'],
            'stats': pokemon['stats'],
            'height': pokemon['height'],
            'weight': pokemon['weight'],
            'id': pokemon['id'],
            'evolutions': listPokemonEvolution,
        }
        listPokemon.append(newDictionary)

    return listPokemon

def getEvolution_chain(evoChain):
    size = len(evoChain)
    for item in range(size):
        pokemon_list = []
        for pokemon in evoChain[item + 1:]:
            dictionary = dict(pokemon)
            pokemon_list.append(dictionary)

        evoChain[item]['evolutions'] = pokemon_list

    return evoChain

def get_SpecieInfo(url_specie):
    response = requests.get(url_specie)
    info_specie = response.json()
    varieties_pokemon = info_specie['varieties']
    specieFullInfo = {}

    if len(varieties_pokemon) > 0:
        url_pokemon = varieties_pokemon[0]['pokemon']['url']
        info_pokemon = get_PokemonInfo(url_pokemon)

        evolves = info_specie['evolves_from_species']

        specieFullInfo['evolves_from_species'] = evolves
        specieFullInfo['name'] = info_pokemon['name']
        specieFullInfo['id'] = info_pokemon['id']
        specieFullInfo['stats'] = info_pokemon['stats']
        specieFullInfo['weight'] = info_pokemon['weight']
        specieFullInfo['height'] = info_pokemon['height']

    return specieFullInfo

def get_PokemonInfo(url_pokemon):
    info_pokemon = requests.get(url_pokemon)
    return info_pokemon.json()

def getAllEvolutions(evoData, evolutionId):
    evoChain = []

    while True:
        evoChain.append({'evolutionChainId': evolutionId,
                         'name': evoData['species']['name'],
                         'url_specie': evoData['species']['url']})

        evoData = evoData['evolves_to']

        if len(evoData) <= 0:
            break
        else:
            evoData = evoData[0]
    return evoChain