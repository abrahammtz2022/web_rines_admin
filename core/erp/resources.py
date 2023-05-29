from import_export import resources
from core.erp.models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product