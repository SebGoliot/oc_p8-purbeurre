from nutella.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from random import randint, choice


def index(request):
    return render(request, 'index.html')

def legal(request):
    return render(request, 'legal.html')


def product(request, product_id):

    product = Product.objects.get(code=product_id)

    ctx = {
        'product_name': product.name,
        'nutriscore': product.nutriscore,
        'product_url': product.product_url,
        'product_img_url': product.image_url,
        'product_reperes': {
            product._meta.get_field('fat').verbose_name: product.fat,
            product._meta.get_field('saturated_fat').verbose_name: product.saturated_fat,
            product._meta.get_field('sugar').verbose_name: product.sugar,
            product._meta.get_field('salt').verbose_name: product.salt,
        },
    }
    return render(request, 'product.html', ctx)


def search(request):
    query = request.GET.get('query')
    product, substitutes = _get_substitutes_from_search(query)
    ctx = {
        'substitutes': substitutes,
        'query': query,
        'query_product': product,
    }
    return render(request, 'search.html', ctx)


def _get_substitutes_from_search(
    search,
) -> "tuple[Product,list[dict]] | tuple[None,None]":

    if product := Product.objects.filter(name__icontains=search).first():
        cat = product.category
        products = Product.objects.filter(category=cat).order_by('nutriscore')

        substitutes = []

        for product in products:
            substitutes.append(
                {
                    'name': product.name,
                    'code': product.code,
                    'nutriscore': product.nutriscore,
                    'product_url': product.product_url,
                    'image_url': product.image_url,
                }
            )

        return (product, substitutes)
    return (None, None)
