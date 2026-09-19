from celery import shared_task
from apps.suppliers.services import update_supplier_products


@shared_task
def update_supplier_products_task():
    update_supplier_products()