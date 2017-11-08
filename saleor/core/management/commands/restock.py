from django.core.management.base import BaseCommand

from saleor.product.models import Stock

class Command(BaseCommand):
    help = 'Replenish the stock in the system'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int)

    def handle(self, *args, **options):
        Stock.objects.all().update(quantity=options['quantity'])
