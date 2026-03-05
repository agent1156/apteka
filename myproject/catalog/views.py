from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator
def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/product_list.html', {'products': page_obj})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return  render(request, 'catalog/product_detail.html', {'product': product})