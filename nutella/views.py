from nutella.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from random import randint, choice


def index(request):
    return render(request, 'index.html')


def product(request, product_id):  # TODO: make real view

    product = Product.objects.get(code=product_id)

    ctx = {
        'product_name': product.name,
        'nutriscore': product.nutriscore,
        'product_url': product.product_url,
        'product_img_url': product.image_url,
        'product_reperes': [ #TODO: Add this to the product model
            "30.9 g Matières grasses / Lipides en quantité élevée",
            "10.6 g Acides gras saturés en quantité élevée",
            "56.3 g Sucres en quantité élevée",
            "0.107 g Sel en faible quantité",
            "Taille d'une portion : 15 g",
        ],
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
