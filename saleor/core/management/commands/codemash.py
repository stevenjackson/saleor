import os
import random

from django.utils.six import moves
from django.core.management.base import BaseCommand

from faker import Factory

from ...utils.random_data import (
    create_product_class_with_attributes,
    get_or_create_category,
    create_product,
    set_product_attributes,
    create_product_images,
    get_variant_combinations,
    get_price_override,
    create_variant)

CODEMASH_SCHEMA = {
    'Hoodie': {
        'category': 'Apparel',
        'product_attributes': {
            'Color': ['Orange'],
            'Brand': ['CodeMash']
        },
        'variant_attributes': {
            'Size': ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        },
        'images_dir': 'hoodies/',
        'is_shipping_required': True
    }
}

class Command(BaseCommand):
    help = 'Create products for CodeMash'
    placeholders_dir = r'saleor/static/placeholders/'

    def handle(self, *args, **options):
        schema = CODEMASH_SCHEMA['Hoodie']
        product_class = create_product_class_with_attributes('Hoodie', schema)
        hoodie = create_product(product_class=product_class, name='CodeMash')
        set_product_attributes(hoodie, product_class)
        category = get_or_create_category('Apparel')
        hoodie.categories.add(category)
        class_placeholders = os.path.join(self.placeholders_dir,
                schema['images_dir'])
        create_product_images(hoodie, 2, class_placeholders)
        variant_combinations = get_variant_combinations(hoodie)

        for i, attr_combination in enumerate(variant_combinations, start=1337):
            sku = '%s-%s' % (hoodie.pk, i)
            create_variant(hoodie, attributes=attr_combination, sku=sku)

        self.stdout.write('Product: %s (%s), %s variant(s)' % (
            hoodie, product_class.name, len(variant_combinations)))

