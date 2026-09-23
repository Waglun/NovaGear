from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.text import slugify


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
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, related_name='products', verbose_name='Бренд')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    sku = models.CharField(max_length=100, blank=True, unique=True, null=True, verbose_name='Артикул')
    # supplier = models.ForeignKey("suppliers.Supplier", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True, verbose_name='Статус категории')

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Статус бренда')

    def get_absolute_url(self):
        return reverse('catalog:brand', kwargs={'brand_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class ProductAttribute(models.Model):
    ATTRIBUTE_TYPES = (
        ('primary', 'Primary Specification'),
        ('secondary', 'Secondary Specification'),
        ('feature', 'Key Feature'),
    )

    attribute_type = models.CharField(
        max_length=20,
        choices=ATTRIBUTE_TYPES,
        default='secondary',
        verbose_name='Тип'
    )

    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE) # Связь многие к одному
    name = models.CharField(max_length=100, verbose_name='Название характеристики')
    value = models.CharField(max_length=255, verbose_name='Значение')
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}: {self.value}"

    class Meta:
        ordering = ('sort_order', 'name')
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return f"{self.product.name} image"

    class Meta:
        ordering = ('sort_order',)
