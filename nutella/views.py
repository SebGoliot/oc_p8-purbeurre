from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from nutella.models import Product, Bookmark

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
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    product, substitutes = _get_substitutes_from_search(query, user)
    ctx = {
        'substitutes': substitutes,
        'query': query,
        'query_product': product,
    }
    return render(request, 'search.html', ctx)


def user_products(request): #TODO this
    return render(request, 'index.html')


def _get_substitutes_from_search( search, user
) -> "tuple[Product,list[dict]] | tuple[None,None]":

    if product := Product.objects.filter(name__icontains=search).first():
        cat = product.category.first()
        products = Product.objects.filter(category=cat).order_by('nutriscore')
        # FIXME flawed logic ? Search gets the first product containing the
        # search string, returns all the products found in the first category

        substitutes = []
        if user :
            user_bookmarks = Bookmark.objects.filter(user=user)
            user_bookmarks = [x.product for x in user_bookmarks]
        else:
            user_bookmarks = []

        for product in products:
            substitutes.append(
                {
                    'name': product.name,
                    'code': product.code,
                    'nutriscore': product.nutriscore,
                    'product_url': product.product_url,
                    'image_url': product.image_url,
                    'is_bookmark': product in user_bookmarks
                }
            )

        return (product, substitutes)
    return (None, None)


def bookmark(request, product_id):
    
    bookmark_state = None
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            product = Product.objects.get(code=product_id)
            bookmark = {
                'user': user,
                'product': product
            }
            try:
                Bookmark.objects.get(**bookmark).delete()
                bookmark_state = False
            except ObjectDoesNotExist:
                Bookmark.objects.create(**bookmark)
                bookmark_state = True

            return JsonResponse({
                "bookmark_state": bookmark_state
                }, status=200)
        else:
            return JsonResponse({
                "bookmark_state": False
                }, status=403)

    raise Http404
