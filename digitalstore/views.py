from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from .forms import LoginForm, RegisterForm, CustomerForm, ShippingForm, EditAccountForm, EditProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import CartForAuthenticatedUser
from shop.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
import stripe


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'digital_store/index.html'
    extra_context = {
        'title': 'Digitalstore'
    }

    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discount_products'] = Product.objects.filter(discount__gt=0)
        context['non_discount_products'] = Product.objects.filter(discount=0).order_by('-created_at')
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'digital_store/product_detail.html'

    # context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=product.category)
        products = [i for i in products if i != product]
        context['products'] = products
        context['title'] = product.title

        return context


def product_by_color(request, color_code, category, brand):
    product = Product.objects.get(color_code=color_code, category__title=category, brand__title=brand)
    products = Product.objects.filter(category=product.category)
    products = [i for i in products if i != product]

    context = {
        'title': product.title,
        'products': products,
        'product': product
    }

    return render(request, 'digital_store/product_detail.html', context)


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digital_store/category_page.html'
    paginate_by = 2

    def get_queryset(self):
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        price_from = self.request.GET.get('from')
        price_until = self.request.GET.get('until')
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)
        if brand:
            products = products.filter(brand__title=brand)
        if color:
            products = products.filter(color_name=color)
        if price_from:
            products = [i for i in products if int(i.price) >= int(price_from)]
        if price_until:
            products = [i for i in products if int(i.price) <= int(price_until)]
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = category.title
        context['category'] = category
        products = Product.objects.filter(category=category)
        context['brands'] = list(set([i.brand for i in products]))
        context['colors'] = list(set([i.color_name for i in products]))
        context['prices'] = [i for i in range(500000, 100000000, 100000)]
        context['color'] = self.request.GET.get('color')
        context['brand'] = self.request.GET.get('brand')
        context['price_from'] = self.request.GET.get('from')
        context['price_until'] = self.request.GET.get('until')

        return context


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')
                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            form = LoginForm()

    context = {
        'title': 'Афторизация',
        'login_form': form
    }

    return render(request, 'digital_store/login.html', context)


def logout_user_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('main')
    else:
        return redirect('main')


def register_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('login')
            else:
                return redirect('register')
        else:
            form = RegisterForm()

        context = {
            'title': 'Регистрация',
            'register_form': form
        }

        return render(request, 'digital_store/register.html', context)


def add_to_favorite_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user
        product = Product.objects.get(slug=slug)
        favorite_products = FavouriteProduct.objects.filter(user=user)
        if user:
            if product in [i.product for i in favorite_products]:
                favorite_product = FavouriteProduct.objects.get(product=product, user=user)
                favorite_product.delete()
            else:
                FavouriteProduct.objects.create(product=product, user=user)

        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


class FavoriteListView(LoginRequiredMixin, ListView):
    model = FavouriteProduct
    context_object_name = 'products'
    template_name = 'digital_store/favorite.html'
    login_url = 'login'
    extra_context = {
        'title': 'Мое избранное'
    }

    def get_queryset(self):
        favorite = FavouriteProduct.objects.filter(user=self.request.user)
        favorite = [i.product for i in favorite]
        return favorite


def add_product_to_cart(request, slug, action):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_cart = CartForAuthenticatedUser(request, slug, action)
        next_page = request.META.get('HTTP_REFERER', 'main')

        return redirect(next_page)


def may_cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart = CartForAuthenticatedUser(request)
        order_info = cart.get_cart_info()
        order_products = order_info['order_products']
        products = Product.objects.all()[::-1][:8]

        context = {
            'title': 'Моя корзина',
            'order': order_info['order'],
            'order_products': order_products
        }

        return render(request, 'digital_store/my_cart.html', context)


def delete_product_from_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        order_product = OrderProduct.objects.all()
        order_product.delete()
        return redirect('my_cart')


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart = CartForAuthenticatedUser(request)
        if cart.get_cart_info()['order_products']:
            regions = Region.objects.all()
            dict_city = {i.pk: [[j.title, j.pk] for j in i.cities.all()] for i in regions}
            context = {
                'title': 'Оформление заказа',
                'order': cart.get_cart_info()['order'],
                'order_products': cart.get_cart_info()['order_products'],
                'customer_form': CustomerForm(instance=request.user.customer),
                'shipping_form': ShippingForm(),
                'dict_city': dict_city
            }
            return render(request, 'digital_store/checkout.html', context)
        else:
            next_page = request.META.get('HTTP_REFERER', 'main')
            return redirect(next_page)


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        stripe.api_key = STRIPE_SECRET_KEY
        if request.method == 'POST':
            cart = CartForAuthenticatedUser(request)
            order_info = cart.get_cart_info()

            customer_form = CustomerForm(data=request.POST)
            shipping_form = ShippingForm(data=request.POST)
            ship_address = ShippingAddress.objects.all()
            if customer_form.is_valid() and shipping_form.is_valid():
                customer = Customer.objects.get(user=request.user)
                customer.first_name = customer_form.cleaned_data['first_name']
                customer.first_name = customer_form.cleaned_data['last_name']
                customer.save()
                address = shipping_form.save(commit=False)
                address.customer = customer
                address.order = order_info['order']
                if order_info['order'] not in [i.order for i in ship_address]:
                    address.save()

            total_price = order_info['order_total_price']
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'rub',
                        'product_data': {'name': 'Товары магазина Digital Store'},
                        'unit_amount': int(total_price / 130) * 100
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('checkout')),
            )

            return redirect(session.url, 303)


def success_payment(request):
    if not request.user.is_authenticated:
        return redirect('main')
    else:
        cart = CartForAuthenticatedUser(request)
        cart.create_payment()

        context = {
            'title': 'Успешная оплата'
        }

        return render(request, 'digital_store/success.html', context)


def profile_info_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)  # Гарантируем, что профиль существует

    try:
        customer = Customer.objects.get(user=user)
        goods = Order.objects.filter(customer=customer, payment=True).order_by('-id')[:1]
    except Customer.DoesNotExist:
        goods = None

    context = {
        'title': f'Профиль {user.username}',
        'profile': profile,
        'items': goods,
    }

    return render(request, 'digital_store/profile_info.html', context)


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)  # Гарантируем, что профиль существует

    if request.method == 'POST':
        account_form = EditAccountForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            return redirect('profile_info')
    else:
        account_form = EditAccountForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

    context = {
        'title': f'Профиль пользователя: {user.username}',
        'account_form': account_form,
        'profile_form': profile_form,
    }

    return render(request, 'digital_store/profile.html', context)


class SearchResult(ListView):
    model = Product
    template_name = 'digital_store/category_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(title__iregex=word)
        return products

