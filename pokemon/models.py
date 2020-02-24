from django.db import models, IntegrityError


# Create your models here.

class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    height = models.CharField(max_length=100, default='')
    weight = models.CharField(max_length=100, default='')

    def savePokemon(self, pokemonDictionary):
        status = True
        try:
            for pokemon in pokemonDictionary:
                pokemon_obj = Pokemon()
                pokemon_obj.name = pokemon['name']
                pokemon_obj.height = pokemon['height']
                pokemon_obj.weight = pokemon['weight']
                pokemon_obj.save()

                self.saveStatistics(pokemon, pokemon_obj)
                self.SaveEvolutions(pokemon, pokemon_obj)
        except IntegrityError as e:
            status = False
        return status

    def SaveEvolutions(self, pokemon, pokemon_obj):
        for evolution in pokemon['evolutions']:
            evolution_pokemon = Evolution()
            evolution_pokemon.pokemon = pokemon_obj
            evolution_pokemon.name = evolution['name']
            evolution_pokemon.evolutionChainId = evolution['evolutionChainId']
            evolution_pokemon.save()

    def saveStatistics(self, pokemon_list, pokemon_obj):
        for stat in pokemon_list['stats']:
            stat_element = StatElement()
            stat_element.pokemon = pokemon_obj
            stat_element.baseStat = stat['base_stat']
            stat_element.effort = stat['effort']
            stat_element.save()

            stats_pokemon = StatsPokemon()
            stats_pokemon.stat = stat_element
            stats_pokemon.name = stat['stat']['name']
            stats_pokemon.url = stat['stat']['url']
            stats_pokemon.save()

class Evolution(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default='')
    evolutionChainId = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')

class StatElement(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default='')
    baseStat = models.CharField(max_length=100, default='')
    effort = models.CharField(max_length=100, default='')

class StatsPokemon(models.Model):
    stat = models.ForeignKey(StatElement, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=100, default='')
    url = models.URLField(max_length=100, default='')