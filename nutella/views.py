from django.http.response import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from nutella.models import Product, Bookmark
from django.contrib.auth.decorators import login_required
from collections import Counter
import json


def index(request):
    """Index view, rendering the index.html template"""
    return render(request, "index.html")


def legal(request):
    """Legal view, rendering the legal.html template"""
    return render(request, "legal.html")


def product(request, product_id):
    """Product view, gets a product and renders the product.html template"""

    product = Product.objects.get(code=product_id)

    ctx = {
        "product_name": product.name,
        "nutriscore": product.nutriscore,
        "product_url": product.product_url,
        "product_img_url": product.image_url,
        "product_reperes": {
            product._meta.get_field("fat").verbose_name: product.fat,
            product._meta.get_field(
                "saturated_fat"
            ).verbose_name: product.saturated_fat,
            product._meta.get_field("sugar").verbose_name: product.sugar,
            product._meta.get_field("salt").verbose_name: product.salt,
        },
    }
    return render(request, "product.html", ctx)


def search(request):
    """Search view, rendering the search.html template with the products found
    with the search query
    """
    if query := request.GET.get("query"):
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        product, substitutes = _get_substitutes_from_search(query, user)
        ctx = {
            "substitutes": substitutes,
            "query": query,
            "query_product": product,
        }
        return render(request, "search.html", ctx)
    else:
        return redirect("index")


def _get_substitutes_from_search(
    search, user
) -> "tuple[Product,list[dict]] | tuple[None,None]":
    """This method retireves and returns the relevant products from a search
    query, and marks the products already saved by the user
    """

    if old_product := Product.objects.filter(name__icontains=search).first():
        # retrieving all the products that shares a category with the query
        categories = old_product.category.all()
        products = []
        for category in categories:
            products += Product.objects.filter(category=category)

        # getting the number of common categories shared
        products_counted = Counter(products).most_common()
        max_categories = products_counted[0][1]

        # keeping only the products that shares the most categories
        products = []
        for each in products_counted:
            if each[1] >= max_categories / 2:
                products.append(each[0])

        # ordering products by nutriscore
        products.sort(key=lambda x: x.nutriscore)

        if user:
            user_bookmarks = Bookmark.objects.filter(user=user)
            user_bookmarks = [x.product for x in user_bookmarks]
        else:
            user_bookmarks = []

        substitutes = []

        for product in products:
            substitutes.append(
                {
                    "name": product.name,
                    "code": product.code,
                    "nutriscore": product.nutriscore,
                    "product_url": product.product_url,
                    "image_url": product.image_url,
                    "is_bookmark": product in user_bookmarks,
                    "old_product_code": old_product.code,
                }
            )

        return (old_product, substitutes)
    return (None, None)


@login_required
def user_products(request):
    """User products view, rendering the bookmarks.html template with the
    products saved by the user
    """
    bookmarks = _get_user_bookmarks(request.user)
    return render(request, "bookmarks.html", {"bookmarks": bookmarks})


def _get_user_bookmarks(user) -> "list[dict] | None":
    """This method retireves and returns all the user's saved products"""

    bookmarks = user.bookmarks.all().order_by("created_at")
    products = []

    for product in bookmarks:
        old_product = product.old_product
        product = product.product
        products.append(
            {
                "name": product.name,
                "code": product.code,
                "nutriscore": product.nutriscore,
                "product_url": product.product_url,
                "image_url": product.image_url,
                "is_bookmark": True,
                "old_product_code": old_product.code,
            }
        )

    return products


def bookmark(request):
    """Bookmark view, used as an AJAX route to handle adding and removing
    bookmarks
    """
    bookmark_state = None
    if request.method == "POST":
        user = request.user

        if user.is_authenticated:

            try:
                json_data = json.loads(request.body.decode())
                old_product_id = json_data.get("old_product_id", None)
                product_id = json_data.get("product_id", None)
                if not old_product_id or not product_id:
                    raise ValueError
            except json.decoder.JSONDecodeError:
                return HttpResponseBadRequest("JSON payload is malformed")
            except ValueError:
                return HttpResponseBadRequest(
                    "JSON payloads is missing some values"
                )

            product = Product.objects.get(code=product_id)
            old_product = Product.objects.get(code=old_product_id)
            bookmark = {
                "user": user,
                "product": product,
                "old_product": old_product,
            }
            try:
                Bookmark.objects.get(**bookmark).delete()
                bookmark_state = False
            except ObjectDoesNotExist:
                Bookmark.objects.create(**bookmark)
                bookmark_state = True

            return JsonResponse({"bookmark_state": bookmark_state}, status=200)
        else:
            return JsonResponse({"bookmark_state": False}, status=403)

    raise Http404
