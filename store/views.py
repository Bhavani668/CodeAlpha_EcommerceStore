from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Order, OrderItem, Product

def home(request):
    return render(request, "home.html", {"products": Product.objects.all()})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

def cart_items(request):
    data = request.session.get("cart", {})
    items, total = [], Decimal("0")
    for pid, qty in data.items():
        product = Product.objects.filter(id=pid).first()
        if product:
            qty = min(int(qty), product.stock)
            subtotal = product.price * qty
            items.append({"product": product, "quantity": qty, "subtotal": subtotal})
            total += subtotal
    return items, total

def cart(request):
    items, total = cart_items(request)
    return render(request, "cart.html", {"items": items, "total": total})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = request.session.get("cart", {})
    key = str(pk)
    data[key] = min(int(data.get(key, 0)) + 1, product.stock)
    request.session["cart"] = data
    messages.success(request, "Product added to cart.")
    return redirect("cart")

def remove_from_cart(request, pk):
    data = request.session.get("cart", {})
    data.pop(str(pk), None)
    request.session["cart"] = data
    return redirect("cart")

@login_required
def checkout(request):
    items, total = cart_items(request)
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("home")
    if request.method == "POST":
        address = request.POST.get("address", "").strip()
        if not address:
            messages.error(request, "Enter delivery address.")
            return render(request, "checkout.html", {"items": items, "total": total})
        order = Order.objects.create(user=request.user, total_amount=total, address=address)
        for item in items:
            OrderItem.objects.create(
                order=order, product=item["product"],
                quantity=item["quantity"], price=item["product"].price
            )
        request.session["cart"] = {}
        messages.success(request, "Order placed successfully.")
        return redirect("orders")
    return render(request, "checkout.html", {"items": items, "total": total})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def orders(request):
    qs = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "orders.html", {"orders": qs})
