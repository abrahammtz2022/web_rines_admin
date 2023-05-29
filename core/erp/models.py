from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name
        
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Sucursal(models.Model):
    numero = models.IntegerField(default=0,verbose_name='Numero Sucursal', unique=True)
    nombre = models.CharField(max_length=80,verbose_name='Nombre Sucursal')
    
    def __str__(self):
        return self.numero
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['id']

        

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=False)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    pcosto = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo de Venta')
    noSucursal = models.IntegerField(default=0,verbose_name='No. de Sucursal')
    nexistencia = models.IntegerField(default=0,verbose_name='Existencia')
    umedida = models.CharField(max_length=20,verbose_name='Unidad de Medida',default='pieza')
    
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        item['exist'] = format(self.nexistencia, '.2f')
        #item['det_prod'] = [i.toJSON() for i in self.cardex_set.all()]
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombre(s)', default='admin')
    surnames = models.CharField(max_length=150, verbose_name='Apellido(s)')
    dni = models.CharField(max_length=13, unique=True, verbose_name='RFC')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento(YYYY-MM-DD)')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%d-%m-%Y')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    sale_username = models.CharField(max_length=100,default='')
    
    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item
    
    def delete(self, using=None, keep_parents=False):
        #DetSale.objects.filter(sale=self)
        print(self.detsale_set.all())
        # cardex = Cardex.objects.filter(prod_sale=self.detsale.id)
        # cardex.prod_estado='C'
        # cardex.prod_cant=0
        # cardex.save()
        for det in self.detsale_set.all():
            #rint(det.cardex.prod_name)
            Cardex.objects.filter(prod_sale=det.sale.id).update(prod_estado='C')
            Cardex.objects.filter(prod_sale=det.sale.id).update(prod_cant=0)
            # cardex = Cardex.objects.filter(prod_sale= det.sale.id)
            # cardex.prod_estado='C'
            # cardex.prod_cant=0
            
            det.prod.nexistencia += det.cant
            det.prod.save()     
        super(Sale, self).delete()
        
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item
    
    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']
        
class Cardex(models.Model):
    prod_id = models.IntegerField(default=0)
    prod_name = models.CharField(max_length=150,  default='')
    prod_costo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    prod_cant = models.IntegerField(default=0)
    prod_fecha = models.DateField(default=datetime.now)
    prod_tipo = models.CharField(max_length=1,  default='V')
    prod_estado = models.CharField(max_length=1,default='R')
    prod_sale = models.IntegerField(default=0)
    prod_user_store = models.IntegerField(default=0)
    prod_user_name = models.CharField(max_length=100,default='')
    
    def __str__(self):
        return self.prod_name
    
    def get_monto_entrada(self):
        if self.prod_tipo == 'C':
            monto = self.prod_cant*self.prod_costo
        else:
            monto=0
        return monto
    
    def get_monto_salida(self):
        if self.prod_tipo == 'V':
            monto = self.prod_cant*self.prod_costo
        else:
            monto=0
        return monto
    
    def get_monto_importe(self):
        if self.prod_tipo == 'V':
            monto = self.prod_cant*self.prod_costo
            monto *= -1
            
        elif self.prod_tipo == 'C':
            monto = self.prod_cant*self.prod_costo
        return monto    
        
  
    def get_total_sal(self):
        if self.prod_tipo == 'V':
            salida = self.prod_cant
        else:
            salida = 0
        return salida
    
    def get_total_entrada(self):
        if self.prod_tipo == 'C':
            entrada = self.prod_cant
        else:
            entrada = 0
        return entrada
    
    def toJSON(self):
        item = model_to_dict(self)
        item['monto_ent'] = self.get_monto_entrada()
        item['monto_sal'] = self.get_monto_salida()
        item['monto_imp'] = self.get_monto_importe()
        item['mov_ent'] = self.get_total_entrada()
        item['mov_sal'] = self.get_total_sal()
       # item['producto'] = self.prod_name
        
        return item
