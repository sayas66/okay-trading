# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
# import Image

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom de la catégorie")
    short_desc = models.CharField(max_length=150, verbose_name="Description courte", blank=True)
    
    def __unicode__(self):
        return self.name
    
    def all_products(self):
#         products = Product.objects.order_by('-id').filter(category_id=self.id,date_validity__gte=datetime.now())
        products = Product.objects.order_by('-id').filter(category_id=self.id,date_validity__gte=datetime.now())
        return products
    
    class Meta:
        verbose_name = 'Categorie'
    
class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name="Nom du produit")
    category = models.ForeignKey(Category, verbose_name="Catégorie du produit")
    short_desc = models.CharField(max_length=150, verbose_name="Description courte", null=True, blank=True)
    long_desc = models.TextField(verbose_name="Description longue", null=True, blank=True)
    price = models.FloatField(verbose_name="Prix du produit")
    transport = models.FloatField(verbose_name="Prix de transport")
    douane = models.FloatField(verbose_name="Douane")
    moq = models.IntegerField(verbose_name="MOQ")
    qty_commanded = models.CharField(max_length=10, default='0', verbose_name="Quantité commandé par les clients", null=True, blank=True)
    thumbnail = models.ImageField(verbose_name="Miniature du produit", upload_to='media/product/', null=True)
    date_added = models.DateField(verbose_name="Date d'ajout", auto_now_add=True)
    date_validity = models.DateField(verbose_name="Date de validité")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Produit'
        
    def get_price(self):
        tva = (self.price * 20) / 100
        return self.price + tva + self.transport
    
    def get_tva(self):
        tva = (self.price * 20) / 100
        return self.price + tva
    
    def get_moq_restant(self):
        x = 0
        if int(self.qty_commanded) < self.moq:
            x = self.moq - int(self.qty_commanded)
        return x

class Address(models.Model):
    user = models.ForeignKey(User)
    
    PARTICULAR = 'Particulier'
    SOCIETY = 'Societe'
    TYPE = (
        (PARTICULAR, 'Particulier'),
        (SOCIETY, 'Societe'),
    )

    MISTER = 'MR'
    MISS = 'MISS'
    MISSES = 'MRS'
    GENDER = (
        (MISTER, 'Monsieur'),
        (MISS, 'Mademoiselle'),
        (MISSES, 'Madame'),
    )
    
    type = models.CharField(max_length=20, default='Particulier', verbose_name="Status", blank=True, null=True, )
    gender = models.CharField(max_length=4, choices=GENDER, default=MISTER, blank=True, null=True, verbose_name="Civilité")
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prénom",)
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom")
    company = models.CharField(max_length=50, blank=True, null=True, verbose_name="Société")
    company_form = models.CharField(max_length=50, blank=True, null=True, verbose_name="Form juridique")
    cin = models.CharField(max_length=12, blank=True, null=True, verbose_name="CIN")
    nif = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIF")
    address = models.CharField(max_length=255, verbose_name="Adresse")
    postcode = models.CharField(max_length=5, verbose_name="Code postal")
    city = models.CharField(max_length=50, verbose_name="Ville")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    
    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'

    def __unicode__(self):
        if self.type == 'Particulier':
            return self.first_name + " " + self.last_name + " (" + self.address + ", " + self.postcode + " " + self.city + ")"
        else:
            return self.company + " " + self.company_form + " (" + self.address + ", " + self.postcode + " " + self.city + ")"

class Cart(models.Model):
    date_now = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()

    def total(self):
        return round(self.product.price * float(self.quantity), 2)
    
    class Meta:
        verbose_name = 'Panier'

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="Client")
    address = models.ForeignKey(Address,
                                         verbose_name="Renseignement de commande",
                                         related_name="order_shipping_address"
                                         )
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    total = models.IntegerField()
    
    order_date = models.DateField(verbose_name="Date de la commande", auto_now=True)
    date_validated = models.DateField(verbose_name='Date de validation', null=True, blank=True)
    
    WAITING = 'En attente'
    VALIDATE = 'Valide'
    CANCELED = 'Anullee'
    STATUS = (
        (WAITING, 'En attente de validation'),
        (VALIDATE, 'Validé'),
        (CANCELED, 'Annulée'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default=WAITING, verbose_name="Statut de la commande")    

    
    def get_tva(self):
        tva = (self.product.price * self.quantity) + ((self.product.price * self.quantity) * 20 / 100)
        return tva
    
    def get_transport(self):
        return self.product.transport * self.quantity
    
    def total(self):
#         t =  round(self.product.price * float(self.quantity), 2)
        self.total = self.get_tva() + self.get_transport()
        return self.get_tva() + self.get_transport()
    
    def get_address(self):
        ad = Address.objects.get(id=self.address.id)
        return ad
    
    def get_product(self):
        p = Product.objects.get(id=self.product.id)
        return p
    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

class OrderSpecial(models.Model):
    user = models.ForeignKey(User, verbose_name="Client")  
    name = models.CharField(max_length=300, verbose_name="Nom du produit")
    short_desc = models.CharField(max_length=150, verbose_name="Description courte", null=True, blank=True)
    long_desc = models.TextField(verbose_name="Description longue", null=True, blank=True)
    thumbnail = models.ImageField(verbose_name="Miniature du produit", upload_to='media/product-special/', null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Quantité commandé")  
    order_date = models.DateField(verbose_name="Date de la commande", auto_now_add=True)
    
    WAITING = 'En attente'
    VALIDATE = 'Valide'
    CANCELED = 'Anullee'
    STATUS = (
        (WAITING, 'En attente de validation'),
        (VALIDATE, 'Validé'),
        (CANCELED, 'Annulée'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default=WAITING, verbose_name="Statut de la commande")    

        
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Commande spéciale'
