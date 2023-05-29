import json
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.erp.forms import SaleForm, ClientForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView

from core.erp.models import Sale, Product, DetSale, Client, Cardex
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                if self.request.user.is_staff == True:
                    data = []
                    for i in Sale.objects.all():
                        data.append(i.toJSON())
                else:
                    data =[]
                    for i in Sale.objects.filter(sale_username=self.request.user):
                        data.append(i.toJSON())
                        
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context


class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                #prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                products = Product.objects.filter(nexistencia__gt=0)
                if len(term):
                    products = products.filter(name__icontains=term)
                    
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    #item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id':term, 'text':term})
                products = Product.objects.filter(name__icontains=term,nexistencia__gt=0)
                #prods = Product.objects.filter(nexistencia__gt=0)
                #if len(term):
                #    prods = prods.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    #item['value'] = i.name
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.sale_username = self.request.user
                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.nexistencia -= det.cant
                        det.prod.save()
                        registro = Cardex()
                        registro.prod_name = det.prod.name
                        registro.prod_costo = det.prod.pcosto
                        registro.prod_cant =int(i['cant'])
                        registro.prod_fecha = vents['date_joined']
                        registro.prod_tipo = 'V'
                        registro.prod_estado = 'R'
                        registro.prod_sale = int(sale.id)
                        registro.prod_id = int(i['id'])
                        registro.prod_user_name = self.request.user
                        registro.save()
                        
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                frmClient = ClientForm(request.POST)
                data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ClientForm()
        return context


class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        instance = self.get_object()
        form = SaleForm(instance=instance)
        form.fields['cli'].queryset = Client.objects.filter(id=instance.cli.id)
        return form
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # if action == 'search_products':
            #     data = []
            #     prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
            #     for i in prods:
            #         item = i.toJSON()
            #         item['value'] = i.name
            #         data.append(item)
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                #prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                products = Product.objects.filter(nexistencia__gt=0)
                if len(term):
                    
                    products = products.filter(name__icontains=term)
                    
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    #item['text'] = i.name
                    data.append(item)                 
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id':term, 'text':term})
                products = Product.objects.filter(name__icontains=term,nexistencia__gt=0)
                #prods = Product.objects.filter(nexistencia__gt=0)
                #if len(term):
                #    prods = prods.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    #item['value'] = i.name
                    item['text'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                        det.prod.stock -= det.cant
                        det.prod.save()
                        registro = Cardex()
                        registro.prod_name = det.prod.name
                        registro.prod_costo = det.prod.pcosto
                        registro.prod_cant =int(i['cant'])
                        registro.prod_fecha = vents['date_joined']
                        registro.prod_tipo = 'V'
                        registro.prod_estado = 'R'
                        registro.prod_sale = int(sale.id)
                        registro.prod_id = int(i['id'])
                        registro.save()
                    data = {'id': sale.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(),default=str)
        context['frmClient'] = ClientForm()
        return context


class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'delete_sale'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class SaleInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # result = finders.find(uri)
        # if result:
        #     if not isinstance(result, (list, tuple)):
        #         result = [result]
        #     result = list(os.path.realpath(path) for path in result)
        #     path = result[0]
        # else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            # template = get_template('sale/invoice.html')
            # context = {
            #     'sale': Sale.objects.get(pk=self.kwargs['pk']),
            #     'comp': {'name': 'PRONORTE J.R.S',
            #              'ruc': '8888888888888888888888', 'address': 'Dajabón,Republica Dominicana'},
            #     'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png')
            # }
            template = get_template('sale/new_ticket.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'empresa': {'direccion':'Av. Jose Maria Morelos 440',
                            'colonia':'David Gustavo Gutierrez Ruiz',
                            'cp':'77013',
                            'localidad':'Chetumal, Quintana Roo',
                            'telefono':'983 123 7040',
                            'nombre_comercial': 'Tienda de Autopartes'},
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:sale_list'))
    
    
class MirarVistaTicket(TemplateView):
    template_name = 'sale/venta_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = 'Eliminación de una Venta'
        context['sale'] = Sale.objects.get(pk=self.kwargs['pk'])
        context['empresa'] = {'direccion':'Av. Jose Maria Morelos 440',
                              'colonia':'David Gustavo Gutierrez Ruiz',
                              'cp':'77013',
                              'localidad':'Chetumal, Quintana Roo',
                              'telefono':'983 123 7040',
                              'nombre_comercial': 'Tienda de Autopartes'}
        return context
    
    