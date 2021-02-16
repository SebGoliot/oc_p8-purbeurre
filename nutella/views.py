from django.shortcuts import render
from random import randint, choice

def index(request):
    return render(request, 'index.html')



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
