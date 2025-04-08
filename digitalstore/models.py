from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Категория')
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, verbose_name='Иконка')
    slug = models.SlugField(unique=True, null=True, verbose_name='Поле слаг')

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return '😁'

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = unidecode(self.title)
            self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    price = models.FloatField(verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='В наличии')
    color_name = models.CharField(max_length=100, verbose_name='Название цвета')
    color_code = models.CharField(max_length=10, verbose_name='Код цвета')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара',
                                 related_name='products')
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг товара')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name='Картинка товара')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления', null=True, blank=True)
    width = models.CharField(max_length=10, verbose_name='Ширина', default='Не указано', null=True, blank=True)
    depth = models.CharField(max_length=10, verbose_name='Глубина', default='Не указано', null=True, blank=True)
    height = models.CharField(max_length=10, verbose_name='Высота', default='Не указано', null=True, blank=True)
    frame = models.CharField(max_length=100, verbose_name='Корпус', default='Не указано', null=True, blank=True)
    accumulator = models.CharField(max_length=100, verbose_name='Аккумулятор', default='Не указано', null=True,
                                   blank=True)
    technology = models.CharField(max_length=100, verbose_name='Технологии', default='Не указано', null=True,
                                  blank=True)
    front_camera = models.CharField(max_length=100, verbose_name='Фронтальная камера', default='Не указано', null=True,
                                    blank=True)
    back_camera = models.CharField(max_length=100, verbose_name='Задняя камера', default='Не указано', null=True,
                                   blank=True)
    os = models.CharField(max_length=100, verbose_name='Операционная система', default='Не указано', null=True,
                          blank=True)
    guarantee = models.CharField(max_length=100, verbose_name='Гарантия', default='Не указано', null=True,
                                 blank=True)
    size = models.IntegerField(verbose_name='Размер', default=0, null=True, blank=True)
    brand = models.ForeignKey('BrandProduct', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Бренд товара')
    discount = models.IntegerField(default=0, null=True, blank=True, verbose_name='Скидка')

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def get_photo(self):
        if self.image:
            return self.image.url
        else:
            return 'https://i.pinimg.com/originals/eb/65/14/eb6514742feb1f01de74e1f00eaf8c96.jpg'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class BrandProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название Бренда (Марка)')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бранд'
        verbose_name_plural = 'Бренды'


class FavouriteProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'Пользователь: {self.user.username} товар {self.product.title}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия покупателя')
    telegram = models.CharField(max_length=100, verbose_name='Телеграм покупателя', null=True, blank=True)

    def __str__(self):
        return f'Покупатель: {self.user.username}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Статус заказа')
    payment = models.BooleanField(default=False, verbose_name='Статус оплаты')
    shopping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return f'Покупатель: {self.customer.first_name} номер заказа {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_order_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])

        return total_price

    @property
    def get_order_total_product(self):
        order_products = self.orderproduct_set.all()
        total_products = sum([product.quantity for product in order_products])
        return total_products


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата измения')

    def __str__(self):
        return f'Товар {self.product.title} заказ №: {self.order.pk}'

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    @property
    def get_order_total_price(self):
        order_products = self.order_product_set.all()
        total_price = sum([product.get_total_price for product in order_products])

        return total_price

    @property
    def get_total_price(self):
        if self.product.discount:
            sum_percent = (self.product.price * self.product.discount) / 100
            self.product.price -= sum_percent

        total_price = self.product.price * self.quantity
        return total_price

    def total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='заказ')
    address = models.CharField(max_length=150, verbose_name='Адрес доставки (улица, дом, кв)')
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    comment = models.TextField(max_length=200, default='Коменарий к заказу', null=True, blank=True,
                               verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, verbose_name='Регион доставки')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Город доставки')

    def __str__(self):
        return f'Заказ номер: {self.order.pk} на имя {self.customer.first_name}'

    class Meta:
        verbose_name = 'Адрес доставок'
        verbose_name_plural = 'Адреса доставок'


class Region(models.Model):
    title = models.CharField(max_length=100, verbose_name='Область')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class City(models.Model):
    title = models.CharField(max_length=100, verbose_name='Город')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион', related_name='cities')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Фото профиля')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, verbose_name='Город', null=True, blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', null=True, blank=True)
    home = models.CharField(max_length=50, verbose_name='Дом', null=True, blank=True)
    flat = models.CharField(max_length=50, verbose_name='Квартира', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_profile_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
