from django.shortcuts import render, get_object_or_404
from .models import Product
from .models import Category
from django.core.paginator import Paginator
def product_list(request,slug=None):
    category = Category.objects.all()
    products = Product.objects.all()
    if slug:
        current_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=current_category)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/product_list.html', {'products': page_obj, 'category': category})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return  render(request, 'catalog/product_detail.html', {'product': product})