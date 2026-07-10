from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Старая цена')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_active = models.BooleanField(default=True, verbose_name='Статус публикации')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name='Бренд')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    sku = models.CharField(max_length=100, blank=True, unique=True, null=True, verbose_name='Артикул')
    # supplier = models.ForeignKey("suppliers.Supplier", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        app_label = 'catalog' # явно указываем ярлык приложения



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE) # Связь многие к одному
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.name}: {self.value}"

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
