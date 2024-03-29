from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q


from .models import Product, Category
from cart.forms import CartAddProductForm
from .recommender import Recommender


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = "product"


class ProductListView(ListView):
    model = Product
    context_object_name = "products"

    template_name = 'shop/product/list.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context


def product_detail_or_list_by_category(request, hierarchy=None):
    category_slug = hierarchy.split("/")
    parent = None
    root = Category.objects.all()
    categories = Category.objects.all()

    cart_product_form = CartAddProductForm()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        product = Category.objects.get(parent=parent, slug=category_slug[-1])
        # r = Recommender()
        # recommended_products = r.suggest_product_for([product], 4)
    except:
        product = get_object_or_404(Product, slug=category_slug[-1])
        r = Recommender()
        recommended_products = r.suggest_products_for([product], 4)

        return render(
            request, "shop/product/detail.html", {
                "product": product, "categories": root, 'cart_product_form': cart_product_form, 'recommended_products': recommended_products}
        )
    else:
        r = Recommender()
        recommended_products = r.suggest_products_for([product], 4)

        context = {
            "product": product,
            "categories": root,
            'recommended_products': recommended_products
        }
        return render(request, "shop/product/categories.html", context=context)


class SearchResultsView(ListView):
    model = Product
    template_name = "shop/product/search_results.html"
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query)
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context
