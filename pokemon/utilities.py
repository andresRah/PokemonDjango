import requests
from pokemon import models
import json


class UtilitiesPokemon:

    urlApi = 'https://pokeapi.co/api/v2/evolution-chain/%s'

    def searchChainByRangeID(self, range_id):
        status = True
        try:
            for index in range(range_id):
                self.searchChainByID(index+1)
        except Exception:
            status = False
        return status

    def searchChainByID(self, chain_id):
        response = requests.get(self.urlApi % str(chain_id))
        chains = response.json()
        evoData = chains['chain']
        evolutionId = chains['id']

        evoChain = self.getAllEvolutions(evoData, evolutionId)

        for pokemon in evoChain:
            info_specie = self.get_SpecieInfo(pokemon['url_specie'])
            pokemon.update(info_specie)

        evoChain = self.getEvolution_chain(evoChain)

        evoChain = self.cleanRespose(evoChain)

        pokemon_model = models.Pokemon()
        status = pokemon_model.savePokemon(evoChain)

        return status, json.dumps(evoChain)

    def cleanRespose(self, evoChain):
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

    def getEvolution_chain(self, evoChain):
        size = len(evoChain)
        for item in range(size):
            pokemon_list = []
            for pokemon in evoChain[item + 1:]:
                dictionary = dict(pokemon)
                pokemon_list.append(dictionary)

            evoChain[item]['evolutions'] = pokemon_list

        return evoChain

    def get_SpecieInfo(self, url_specie):
        response = requests.get(url_specie)
        info_specie = response.json()
        varieties_pokemon = info_specie['varieties']
        specieFullInfo = {}

        if len(varieties_pokemon) > 0:
            url_pokemon = varieties_pokemon[0]['pokemon']['url']
            info_pokemon = self.get_PokemonInfo(url_pokemon)

            evolves = info_specie['evolves_from_species']

            specieFullInfo['evolves_from_species'] = evolves
            specieFullInfo['name'] = info_pokemon['name']
            specieFullInfo['id'] = info_pokemon['id']
            specieFullInfo['stats'] = info_pokemon['stats']
            specieFullInfo['weight'] = info_pokemon['weight']
            specieFullInfo['height'] = info_pokemon['height']

        return specieFullInfo

    def get_PokemonInfo(self, url_pokemon):
        info_pokemon = requests.get(url_pokemon)
        return info_pokemon.json()

    def getAllEvolutions(self, evoData, evolutionId):
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