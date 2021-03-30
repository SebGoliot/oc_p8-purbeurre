from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from nutella.models import Product, Bookmark

def index(request):
    """ Index view, rendering the index.html template
    """
    return render(request, 'index.html')

def legal(request):
    """ Legal view, rendering the legal.html template
    """
    return render(request, 'legal.html')


def product(request, product_id):
    """ Product view, gets a product and renders the product.html template
    """

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
    """ Search view, rendering the search.html template with the products found
    with the search query
    """
    if query := request.GET.get('query'):
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
    else:
        return redirect('index')


def user_products(request): #TODO this
    """ User products view, rendering the bookmarks.html template with the
    products saved by the user
    """
    return render(request, 'index.html')


def _get_substitutes_from_search( search, user
) -> "tuple[Product,list[dict]] | tuple[None,None]":
    """ This method retireves and returns the relevant products from a search
    query, and marks the products already saved by the user
    """

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
    """ Bookmark view, used as an AJAX route to handle adding and removing
    bookmarks
    """
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
