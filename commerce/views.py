# -*- coding:utf-8 -*-

from commerce.models import *
from commerce.forms import *

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from io import BytesIO
from django.contrib.auth.models import User

import datetime
import random
from datetime import date
import time

# Create your views here.

def slide_all_product():
    products = list()
    count = Product.objects.count()
    p = Product.objects.order_by('price').filter(date_validity__gte=datetime.datetime.now())
    i = 0
    while i < count:
        products.append(p[i:(i+3)])
        i += 3

    return products

def initialize_product_data():
    products = Product.objects.all()
    for product in products:
        if datetime.date.today().__ge__(product.date_validity):
            product.qty_commanded = 0
            product.save()

def splash(request):
    return render(request, 'spash.html')

def index(request):
    products = Product.objects.order_by('-id').filter(date_validity__gte=datetime.datetime.now())
    products_slide = slide_all_product()
    categories_list = Category.objects.all()

    address_count = Address.objects.filter(user_id=request.user.id).count()
    if request.user.is_authenticated():
        if request.user.is_superuser:
            user_count = User.objects.all().count() - 1
            orders = Order.objects.order_by('-id').filter()
            orders_valide = Order.objects.filter(status='Valide').order_by('-date_validated')
            orders_waite = Order.objects.filter(status='En attente').order_by('-date_validated')
            initialize_product_data()
            return render(request, 'admin_okay/index.html', locals())
        else:
            order_special = OrderSpecial.objects.filter(user_id=request.user.id, status='Valide').count()
            if order_special > 0:
                messages.add_message(request, messages.INFO, "Vous avez des commandes spéciale validé <br>\
                Nous vous informons par e-mail la suite de votre commande spéciale")
    
    return render(request, 'index.html', locals())

# -------------------------------------
# user connexion
# -------------------------------------

def information(request):
    products = Product.objects.filter(date_validity__lte=datetime.datetime.now()).order_by('-id')[:6]
    products_slide = slide_all_product()
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    return render(request, 'information.html', locals())

def condition(request):
    products = Product.objects.filter(date_validity__lte=datetime.datetime.now()).order_by('-id')[:6]
    products_slide = slide_all_product()
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    return render(request, 'condition.html', locals())

class SignUpView(generic.CreateView):
    form_class = UsersCreationForm
    model = User
    success_url = reverse_lazy('commerce:index')
    template_name = 'account/sign_up.html'
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO,
                             'Vous ête actuellement membre du site! Connectez à votre compte à fin d\'effectuer des commandes')
        return super(SignUpView, self).form_valid(form)
    
class SignInView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('commerce:index')
    template_name = 'account/sign_in.html'
    
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            login(self.request, user)
            return super(SignInView, self).form_valid(form)
        else:
            return self.form_invalid(form)
        
class SignOutView(generic.RedirectView):
    url = reverse_lazy('sign_in')
    
    def get(self, request):
        logout(request)
        return super(SignOutView, self).get(request)

def account(request):
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        
#         if user.check_password(request.POST['password1']):
#             user.set_password(request.POST['password2'])
#         else:
#             messages.add_message(request, messages.ERROR, "Password invalide. Veuillez saisir votre ancien password")
        
        user.save()
        
    return render(request, 'account/account.html', locals())

# product & category

def display_category(request, category_id):
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    category = get_object_or_404(Category, pk=category_id)
    product_list = category.all_products()
    paginator = Paginator(product_list, 12)
    products_slide = slide_all_product()
 
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
 
    return render(request, 'commerce/category.html', locals())

def display_category_random(request):
    categories_list = Category.objects.all()
    x = random.randint(0, categories_list.count()-1)
    category_id = categories_list[x].id
    category = get_object_or_404(Category, pk=category_id)
    product_list = category.all_products()
    paginator = Paginator(product_list, 4)
    products_slide = slide_all_product()
 
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
 
    return render(request, 'commerce/category.html', locals())

def display_product_min_price(request):
    title = 'Produits moins chère'
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
#     product_list = Product.objects.order_by('price')
    product_list = Product.objects.order_by('price').filter(date_validity__gte=datetime.datetime.now())
    paginator = Paginator(product_list, 12)
    products_slide = slide_all_product()
 
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
 
    return render(request, 'commerce/product_min.html', locals())

def display_product_min_moq(request):
    title = 'Produit avec une MOQ minimum'
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
#     product_list = Product.objects.order_by('moq')
    product_list = Product.objects.order_by('moq').filter(date_validity__gte=datetime.datetime.now())
    paginator = Paginator(product_list, 12)
    products_slide = slide_all_product()
 
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
 
    return render(request, 'commerce/product_min.html', locals())


def display_product(request, product_id):
#     id = request.session['cart'].get('product_qty')
    product = get_object_or_404(Product, pk=product_id) 
    products_slide = slide_all_product()
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    
    if request.method == 'POST':
        quantity = request.POST['quantity']        
        if Cart.objects.filter(user_id=request.user.id, product_id=product_id).exists():
            cart = Cart.objects.get(user_id=request.user.id, product_id=product_id)
            cart.quantity = request.POST['quantity']
        else:
            cart = Cart(user_id=request.user.id, product_id=product_id, quantity=int(request.POST['quantity']))

        cart.save()
                
        return render(request, 'commerce/cart.html', locals())
    
    return render(request, 'commerce/product.html', locals())

# orders

def confirmation(request):
    pass

def shipping(request, product_id):
    categories_list = Category.objects.all()
    addresses = Address.objects.filter(user_id=request.user.id)
    cart = Cart.objects.get(user_id=request.user.id, product_id=product_id)
    
    if request.method == 'POST':
        order = Order(product_id=product_id,
                      user_id=request.user.id,
                      address_id=request.POST['shipping_address'],
                      quantity=cart.quantity)
        
        product = Product.objects.get(id=product_id)
        x = int(product.qty_commanded) + int(cart.quantity)
        product.qty_commanded = str(x)
        
        if x < product.moq:
            order.status = 'En attente'
        else:
            order.status = 'Valide'
            order.date_validated = datetime.datetime.now()
            l = Order.objects.filter(product_id=product_id, status='En attente')
            for l1 in l:
                l1.date_validated = datetime.datetime.now()
                l1.status = 'Valide'
                l1.save()
#                 if product.date_validity >= datetime.datetime.now():
#                     product.qty_commanded = 0
         
        product.save()
        order.save()
        
        messages.add_message(request, messages.INFO, "Cliquer sur l'icone impression de votre commande pour obtenir le contrat.")
        
        if int(product.qty_commanded) < product.moq:
            messages.add_message(request, messages.INFO, "Votre commande sera validé quand la MOQ de ce produit sera atteinte")
        else:
            messages.add_message(request, messages.INFO, "Votre commande a été validé")
        
        return redirect('commerce:display_order')
    
    if request.GET.get('next', False):
        return redirect(request.GET['next'])
    else:
        return render(request, 'commerce/shipping.html', locals())
    
#     return render(request, 'commerce/shipping.html', locals())

@login_required(login_url='account/sign-in')
def add_address(request):
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    if request.method == 'POST':
        add_address_form = AddAddress(request.POST)
        if add_address_form.is_valid():
            user = request.user
            address = add_address_form.save(commit=False)
            address.user_id = user.id
            address.type = request.POST['client_status']
            address.save()
            messages.add_message(request, messages.SUCCESS, "Votre renseignement de commande à été ajouté avec succès")
            if request.GET.get('next', False):
                return redirect(request.GET['next'])
            else:
                redirect('commerce:addresses')
#             return redirect(reverse('commerce:shipping'), locals())
#             return redirect('commerce:addresses')
        else:
            messages.add_message(request, messages.ERROR, "Verifier les champs saisies")
    else:
        add_address_form = AddAddress()
    return render(request, 'account/add_address.html', locals())
#     return redirect(request.META.get('HTTP_REFERER'))

@login_required()
def remove_address(request, address_id):
    Address.objects.get(id=address_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='account/sign-in')
def addresses(request):
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
#     client = Client.objects.get(user_id=request.user.id)
    addresses = Address.objects.filter(user_id=request.user.id)
    return render(request, 'account/addresses.html', locals())

@login_required(login_url='account/sign-in')
def display_order(request):    
#     orders_list = Order.objects.filter(user_id=request.user.id).order_by('-id', 'date_validated')
    orders_list = Order.objects.filter(user_id=request.user.id).order_by('-id')
    orders_valide = Order.objects.filter(user_id=request.user.id,status='Valide').order_by('date_validated')
    orders_waite = Order.objects.filter(user_id=request.user.id,status='En attente').order_by('-id')
    orders_special = OrderSpecial.objects.filter(user_id=request.user.id).order_by('-id')
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    
    paginator = Paginator(orders_list, 9)
 
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    return render(request, 'account/order.html', locals())

@login_required(login_url='account/sign-in')
def display_order_special(request):    
#     orders_list = Order.objects.filter(user_id=request.user.id).order_by('-id', 'date_validated')
    orders_list = OrderSpecial.objects.filter(user_id=request.user.id).order_by('-id')
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()
    
    paginator = Paginator(orders_list, 9)
 
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    return render(request, 'account/order-special.html', locals())

@login_required(login_url='account/sign-in')
def add_to_cart(request, product_id, qty):
    categories_list = Category.objects.all()
    product = Product.objects.get(id=product_id)
    return render(request, 'commerce/cart.html', locals())

def print_contrat(request, order_id):
    order = Order.objects.get(id=order_id)
    response = HttpResponse(content_type='application/pdf')
    filename = "OKay-Commande-%s.pdf" % datetime.datetime.now()
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
 
    buffer = BytesIO()
 
    report = MyPrint(buffer, 'Letter', request.user, order)
    pdf = report.print_users()
 
    response.write(pdf)
    return response

class MyPrint:
    def __init__(self, buffer, pagesize, user, order):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        self.user = user
        self.order = order
        
    def print_users(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)
        
        elements = []
#         footer1 = "<b>1.</b> La durée de validité de cette souscription est de ... <b>2.</b> OKAY TRADING mettra tout en oeuvre afin de faire d'atteindre le MOQ nécessaire au lancement de la commande. <b>3.</b> Le client s'engage a honorer la souscription en cas d'atteinte des MOQ. Je m'engage a honoré cette soscription en cas d'atteinte des MOQ"
        footer1 = "<b>1.</b> OKAY TRADING mettra tout en oeuvre afin de faire d'atteindre le MOQ nécessaire au lancement de la commande. <b>2.</b> Le client s'engage a honorer la souscription en cas d'atteinte des MOQ. Je m'engage a honoré cette soscription en cas d'atteinte des MOQ"
        footer2 = "OKAY TRADING - SOCIETE A RESPONSABILITE LIMITE AU CAPITAL DE 2.000.000 MGA"
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        
        logo = 'logo.png'
        elements.append(Image(logo, 40*mm, 25*mm))
        elements.append(Spacer(0, 50))
        
        info = 'Commande passée le %s' % self.order.order_date
        elements.append(Paragraph(info, styles['Normal']))
        elements.append(Spacer(0, 10))
        
        if self.order.get_address().type == 'Particulier':
            info1 = '%s %s' % (self.order.get_address().last_name, self.order.get_address().first_name)
        elif self.order.get_address().type == 'Societe':
            info1 = '%s %s' % (self.order.get_address().company, self.order.get_address().company_form)
#         elements.append(Paragraph(self.user.get_full_name(), styles['Heading3']))
        elements.append(Paragraph(info1, styles['Heading3']))
        elements.append(Paragraph(self.order.get_address().address, styles['Normal']))
        
        info2 = '%s %s' % (self.order.get_address().city, self.order.get_address().postcode)
        elements.append(Paragraph(info2, styles['Normal']))
        elements.append(Spacer(0, 10))
        
        info3 = 'Produit : %s' % self.order.get_product().name
        elements.append(Paragraph(info3, styles['Normal']))
        
        info4 = 'Description : %s' % self.order.get_product().short_desc
        elements.append(Paragraph(info4, styles['Normal']))
        
        info5 = 'Prix unitaire : %s MGA' % self.order.get_product().price
        elements.append(Paragraph(info5, styles['Normal']))

        info6 = 'Quantité demandé : %s' % self.order.quantity
        elements.append(Paragraph(info6, styles['Normal']))
        
        info7 = 'Transport : %s MGA' % self.order.get_transport()
        elements.append(Paragraph(info7, styles['Normal']))
        
        info8 = 'TVA 20% : {} MGA'.format(self.order.get_tva())
        elements.append(Paragraph(info8, styles['Normal']))
        
        info9 = 'Prix total : %s MGA' % self.order.total()
        elements.append(Paragraph(info9, styles['Normal']))
        
        elements.append(Spacer(0, 50))
        image = self.order.get_product().thumbnail
        elements.append(Image(image, 40*mm, 40*mm))
        
        elements.append(Spacer(0, 80))
        elements.append(Paragraph(footer1, styles['Normal']))
        elements.append(Spacer(0, 20))
        elements.append(Paragraph(footer2, styles['Normal']))
        
        doc.build(elements)
        
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

# admin

def users_order_special_validate(request, id):
    current_order = OrderSpecial.objects.get(id=id)
    current_order.status = 'Valide'
    current_order.save()
    
    orders = OrderSpecial.objects.all().order_by('status')
    user_count = User.objects.all().count() - 1 
    return render(request, 'admin_okay/order-special.html', locals())

def display_users(request):
    users = User.objects.all()
    user_count = users.count() - 1 
    return render(request, 'admin_okay/user_list.html', locals())

def display_users_order_special(request):
    orders = OrderSpecial.objects.all()
    user_count = User.objects.all().count() - 1 
    return render(request, 'admin_okay/order-special.html', locals())

def display_users_order(request, id):
    client = User.objects.get(id=id)
    user_count = User.objects.all().count()
    orders_list = Order.objects.filter(user_id=id).order_by('-id')
    orders_valide = Order.objects.filter(user_id=id,status='Valide').order_by('date_validated')
    orders_waite = Order.objects.filter(user_id=id,status='En attente').order_by('-id')
    
    paginator = Paginator(orders_list, 9)
 
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_okay/order.html', locals())

@login_required(login_url='account/sign-in')
def shipping_special(request):
    products_slide = slide_all_product()
    categories_list = Category.objects.all()
    address_count = Address.objects.filter(user_id=request.user.id).count()

    if request.method == 'POST':
        form = OrderSpecialForm(request.POST)
        if form.is_valid():
            user = request.user
            order = form.save(commit=False)
            order.user_id = user.id
            order.save()
            messages.add_message(request, messages.SUCCESS, "Votre commande à été enregistrer.")
            if request.GET.get('next', False):
                return redirect(request.GET['next'])
            else:
                redirect('commerce:addresses')
        else:
            messages.add_message(request, messages.ERROR, "Verifier les champs saisies")
    else:
        form = OrderSpecialForm()
    return render(request, 'commerce/shipping-special.html', locals())