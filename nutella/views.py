from django.shortcuts import render
from random import randint, choice

def index(request):
    return render(request, 'index.html')



def product(request):
    query = request.GET.get('product_id')

    ctx = {
        'product_name': "Nutella",
        'nutriscore': "c",
        'product_img_url': 'https://static.openfoodfacts.org/images/products/301/762/040/6003/front_fr.130.200.jpg',
        'product_reperes': [
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
    substitutes = get_products_from_search(query)
    ctx = {
        'substitutes': substitutes,
        'query' : query,
        'query_img_url': 'https://static.openfoodfacts.org/images/products/301/762/040/6003/front_fr.130.200.jpg',
        }
    return render(request, 'search.html', ctx)


def get_products_from_search(search) -> "list[dict]":
    img_url = 'https://static.openfoodfacts.org/images/products/301/762/040/6003/front_fr.130.200.jpg'

    substitutes = []
    score_list = ['A','B','C','D','E',]
    for each in range(randint(0, 16)):
        substitutes.append(
            {
                'id': each,
                'name': search,
                'image_url': img_url,
                'nutriscore': choice(score_list),
                'name': "woah"
            })

    return substitutes
