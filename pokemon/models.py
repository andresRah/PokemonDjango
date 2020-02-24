from django.db import models
# Create your models here.

class Evolution(models.Model):
    evolutionChainId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

class StatsPokemon(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=100)

class StatElement(models.Model):
    stat = models.ForeignKey(StatsPokemon, on_delete=models.CASCADE)
    baseStat = models.CharField(max_length=100)
    effort = models.CharField(max_length=100)

class Pokemon(models.Model):
    stats = models.ForeignKey(StatsPokemon, on_delete=models.CASCADE)
    evolutions = models.ForeignKey(Evolution, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)

    def savePokemon(self, pokemonDictionary):
        ki = pokemonDictionary
