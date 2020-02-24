from django.core.management.base import BaseCommand
from django.utils import timezone
from pokemon import utilities


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('evolutionChainID',
                            nargs='+',
                            type=int,
                            default=1,
                            help='EvolutionChainID parameter')

    def handle(self, *args, **kwargs):
        chain_id = kwargs['evolutionChainID']

        time = timezone.now().strftime('%X')
        self.stdout.write(self.style.WARNING("Begin....  %s" % time))
        self.stdout.write(self.style.WARNING("Begin....  %s" % chain_id))

        utilities_pokemon = utilities.UtilitiesPokemon()
        response_utility = utilities_pokemon.searchChainByID(chain_id[0])
        status = response_utility[0]

        if status:
            self.stdout.write(self.style.SUCCESS("Register created.... %s" % time))
        else:
            self.stdout.write(self.style.WARNING("Register already exists.... %s" % time))

        json_evolution_chain = response_utility[1]
        self.stdout.write(json_evolution_chain)

        time = timezone.now().strftime('%X')

        self.stdout.write(self.style.SUCCESS("Success.... %s" % time))