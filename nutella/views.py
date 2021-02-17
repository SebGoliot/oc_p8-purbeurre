from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from random import randint, choice


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def account(request): #TODO: make real view
    query = request.GET.get('username')

    ctx = {
        'username': query,
        'user_mail': query + "@gmail.com", 
        }
    return render(request, 'account.html', ctx)


def product(request): #TODO: make real view
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


def search(request): #TODO: make real view
    query = request.GET.get('query')
    substitutes = get_products_from_search(query)
    ctx = {
        'substitutes': substitutes,
        'query' : query,
        'query_img_url': 'https://static.openfoodfacts.org/images/products/301/762/040/6003/front_fr.130.200.jpg',
        }
    return render(request, 'search.html', ctx)


def get_products_from_search(search) -> "list[dict]": #TODO: make real view
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
