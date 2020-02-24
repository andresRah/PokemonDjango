from django.core.management.base import BaseCommand
from django.utils import timezone
from pokemon import utilities


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('evolutionChainRangeID',
                            nargs='+',
                            type=int,
                            default=1,
                            help='EvolutionChainRangeID parameter')

    def handle(self, *args, **kwargs):
        range_chain_id = kwargs['evolutionChainRangeID']

        time = timezone.now().strftime('%X')
        self.stdout.write(self.style.WARNING("Begin....  %s" % time))
        self.stdout.write(self.style.WARNING("Begin.... Range chain ID ...  %s" % range_chain_id))

        utilities_pokemon = utilities.UtilitiesPokemon()
        status = utilities_pokemon.searchChainByRangeID(range_chain_id[0])

        if status:
            self.stdout.write(self.style.SUCCESS("Register created.... %s" % time))
        else:
            self.stdout.write(self.style.WARNING("Register already exists.... %s" % time))

        time = timezone.now().strftime('%X')

        self.stdout.write(self.style.SUCCESS("Success.... %s" % time))