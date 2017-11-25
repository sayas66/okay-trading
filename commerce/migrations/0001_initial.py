# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'Particulier', max_length=20, null=True, verbose_name=b'Status', blank=True)),
                ('gender', models.CharField(default=b'MR', choices=[(b'MR', b'Monsieur'), (b'MISS', b'Mademoiselle'), (b'MRS', b'Madame')], max_length=4, blank=True, null=True, verbose_name=b'Civilit\xc3\xa9')),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name=b'Pr\xc3\xa9nom', blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name=b'Nom', blank=True)),
                ('company', models.CharField(max_length=50, null=True, verbose_name=b'Soci\xc3\xa9t\xc3\xa9', blank=True)),
                ('company_form', models.CharField(max_length=50, null=True, verbose_name=b'Form juridique', blank=True)),
                ('cin', models.CharField(max_length=12, null=True, verbose_name=b'CIN', blank=True)),
                ('nif', models.CharField(max_length=50, null=True, verbose_name=b'NIF', blank=True)),
                ('address', models.CharField(max_length=255, verbose_name=b'Adresse')),
                ('postcode', models.CharField(max_length=5, verbose_name=b'Code postal')),
                ('city', models.CharField(max_length=50, verbose_name=b'Ville')),
                ('phone', models.CharField(max_length=20, verbose_name=b'T\xc3\xa9l\xc3\xa9phone')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Adresse',
                'verbose_name_plural': 'Adresses',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_now', models.DateField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Panier',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name=b'Nom de la cat\xc3\xa9gorie')),
                ('short_desc', models.CharField(max_length=150, verbose_name=b'Description courte', blank=True)),
            ],
            options={
                'verbose_name': 'Categorie',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('order_date', models.DateField(auto_now=True, verbose_name=b'Date de la commande')),
                ('date_validated', models.DateField(null=True, verbose_name=b'Date de validation', blank=True)),
                ('status', models.CharField(default=b'En attente', max_length=10, verbose_name=b'Statut de la commande', choices=[(b'En attente', b'En attente de validation'), (b'Valide', b'Valid\xc3\xa9'), (b'Anullee', b'Annul\xc3\xa9e')])),
                ('address', models.ForeignKey(related_name='order_shipping_address', verbose_name=b'Renseignement de commande', to='commerce.Address')),
            ],
            options={
                'verbose_name': 'Commande',
                'verbose_name_plural': 'Commandes',
            },
        ),
        migrations.CreateModel(
            name='OrderSpecial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name=b'Nom du produit')),
                ('short_desc', models.CharField(max_length=150, null=True, verbose_name=b'Description courte', blank=True)),
                ('long_desc', models.TextField(null=True, verbose_name=b'Description longue', blank=True)),
                ('thumbnail', models.ImageField(upload_to=b'media/product-special/', null=True, verbose_name=b'Miniature du produit', blank=True)),
                ('quantity', models.IntegerField(verbose_name=b'Quantit\xc3\xa9 command\xc3\xa9')),
                ('order_date', models.DateField(auto_now_add=True, verbose_name=b'Date de la commande')),
                ('status', models.CharField(default=b'En attente', max_length=10, verbose_name=b'Statut de la commande', choices=[(b'En attente', b'En attente de validation'), (b'Valide', b'Valid\xc3\xa9'), (b'Anullee', b'Annul\xc3\xa9e')])),
                ('user', models.ForeignKey(verbose_name=b'Client', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Commande sp\xe9ciale',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name=b'Nom du produit')),
                ('short_desc', models.CharField(max_length=150, null=True, verbose_name=b'Description courte', blank=True)),
                ('long_desc', models.TextField(null=True, verbose_name=b'Description longue', blank=True)),
                ('price', models.FloatField(verbose_name=b'Prix du produit')),
                ('transport', models.FloatField(verbose_name=b'Prix de transport')),
                ('douane', models.FloatField(verbose_name=b'Douane')),
                ('moq', models.IntegerField(verbose_name=b'MOQ')),
                ('qty_commanded', models.CharField(default=b'0', max_length=10, null=True, verbose_name=b'Quantit\xc3\xa9 command\xc3\xa9 par les clients', blank=True)),
                ('thumbnail', models.ImageField(upload_to=b'media/product/', null=True, verbose_name=b'Miniature du produit')),
                ('date_added', models.DateField(auto_now_add=True, verbose_name=b"Date d'ajout")),
                ('date_validity', models.DateField(verbose_name=b'Date de validit\xc3\xa9')),
                ('category', models.ForeignKey(verbose_name=b'Cat\xc3\xa9gorie du produit', to='commerce.Category')),
            ],
            options={
                'verbose_name': 'Produit',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='commerce.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(verbose_name=b'Client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(to='commerce.Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
