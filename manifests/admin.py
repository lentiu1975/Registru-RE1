from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import ManifestEntry, DatabaseYear, ContainerType, Ship, Pavilion
from datetime import datetime


class CustomDateWidget(DateWidget):
    """Widget custom pentru format de data DD.MM.YYYY"""
    def clean(self, value, row=None, **kwargs):
        if not value:
            return None

        # Daca este deja un obiect date, returneaza-l
        if isinstance(value, datetime):
            return value.date()

        # Incearca sa parseze data in format DD.MM.YYYY
        if isinstance(value, str):
            for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%Y-%m-%d']:
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue

        return super().clean(value, row, **kwargs)


class ManifestEntryResource(resources.ModelResource):
    """Resource pentru import/export Excel"""

    # Mapare coloane Excel -> Model Django
    numar_manifest = Field(attribute='numar_manifest', column_name='numar manifest')
    numar_permis = Field(attribute='numar_permis', column_name='numar permis')
    numar_pozitie = Field(attribute='numar_pozitie', column_name='numar pozitie')
    cerere_operatiune = Field(attribute='cerere_operatiune', column_name='cerere operatiune')
    data_inregistrare = Field(attribute='data_inregistrare', column_name='data inregistrare', widget=CustomDateWidget(format='%d.%m.%Y'))
    container = Field(attribute='container', column_name='container')
    numar_colete = Field(attribute='numar_colete', column_name='numar colete')
    greutate_bruta = Field(attribute='greutate_bruta', column_name='greutate bruta')
    descriere_marfa = Field(attribute='descriere_marfa', column_name='descriere marfa')
    tip_operatiune = Field(attribute='tip_operatiune', column_name='tip operatiune')
    nume_nava = Field(attribute='nume_nava', column_name='nume nava')
    pavilion_nava = Field(attribute='pavilion_nava', column_name='pavilion nava')
    numar_sumara = Field(attribute='numar_sumara', column_name='numar sumara')
    tip_container = Field(attribute='tip_container', column_name='tip container')
    linie_maritima = Field(attribute='linie_maritima', column_name='linie maritima')

    class Meta:
        model = ManifestEntry
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['numar_manifest', 'numar_pozitie', 'container']
        fields = (
            'numar_manifest', 'numar_permis', 'numar_pozitie', 'cerere_operatiune',
            'data_inregistrare', 'container', 'numar_colete', 'greutate_bruta',
            'descriere_marfa', 'tip_operatiune', 'nume_nava', 'pavilion_nava', 'numar_sumara',
            'tip_container', 'linie_maritima', 'model_container'
        )

    def before_import_row(self, row, **kwargs):
        """Genereaza numar_curent automat inainte de import"""
        # Get max numar_curent din baza de date
        max_numar = ManifestEntry.objects.aggregate(models.Max('numar_curent'))['numar_curent__max']
        if max_numar is None:
            max_numar = 0
        # Nu incrementam aici, o facem in after_import_row pentru fiecare rand nou

    def after_import_row(self, row, row_result, **kwargs):
        """Seteaza numar_curent pentru randurile noi sau actualizate"""
        if row_result.import_type in ['new', 'update']:
            instance = row_result.instance
            if instance and instance.pk:
                # Daca e nou, setam numar_curent
                if instance.numar_curent == 0:
                    max_numar = ManifestEntry.objects.aggregate(models.Max('numar_curent'))['numar_curent__max']
                    if max_numar is None:
                        max_numar = 0
                    instance.numar_curent = max_numar + 1
                    instance.save(update_fields=['numar_curent'])


# Admin actions globale - trebuie definite INAINTE de clase
def sync_lookup_tables_action(modeladmin, request, queryset):
    """Actiune admin pentru sincronizarea tabelelor de referinta"""
    from django.core.management import call_command
    from io import StringIO

    # Capteaza output-ul command-ului
    out = StringIO()
    call_command('sync_lookup_tables', stdout=out)
    output = out.getvalue()

    # Afiseaza output-ul ca mesaj de succes
    modeladmin.message_user(request, output)

sync_lookup_tables_action.short_description = 'Sincronizeaza tabele (ContainerType, Ship, Pavilion)'


@admin.register(ManifestEntry)
class ManifestEntryAdmin(ImportExportModelAdmin):
    """Admin pentru ManifestEntry cu import/export Excel"""

    resource_class = ManifestEntryResource
    actions = [sync_lookup_tables_action]

    list_display = [
        'format_numar_curent',
        'format_numar_manifest', 'format_numar_permis', 'format_numar_pozitie', 'format_cerere_operatiune',
        'format_data_inregistrare', 'container', 'format_model_container', 'format_tip_container',
        'format_numar_colete', 'format_greutate_bruta', 'format_descriere_marfa', 'format_tip_operatiune',
        'format_nume_nava', 'format_pavilion_nava', 'format_numar_sumara', 'format_linie_maritima'
    ]

    def format_numar_curent(self, obj):
        return obj.numar_curent
    format_numar_curent.short_description = format_html('Nr.<br>Crt.')
    format_numar_curent.admin_order_field = 'numar_curent'

    def format_data_inregistrare(self, obj):
        """Formatare data in DD.MM.YYYY"""
        if obj.data_inregistrare:
            return obj.data_inregistrare.strftime('%d.%m.%Y')
        return '-'
    format_data_inregistrare.short_description = format_html('Data<br>Inregistrare')
    format_data_inregistrare.admin_order_field = 'data_inregistrare'

    def format_numar_manifest(self, obj):
        return obj.numar_manifest
    format_numar_manifest.short_description = format_html('Numar<br>Manifest')
    format_numar_manifest.admin_order_field = 'numar_manifest'

    def format_numar_permis(self, obj):
        return obj.numar_permis
    format_numar_permis.short_description = format_html('Numar<br>Permis')
    format_numar_permis.admin_order_field = 'numar_permis'

    def format_numar_pozitie(self, obj):
        return obj.numar_pozitie
    format_numar_pozitie.short_description = format_html('Numar<br>Pozitie')
    format_numar_pozitie.admin_order_field = 'numar_pozitie'

    def format_cerere_operatiune(self, obj):
        return obj.cerere_operatiune
    format_cerere_operatiune.short_description = format_html('Cerere<br>Operatiune')
    format_cerere_operatiune.admin_order_field = 'cerere_operatiune'

    def format_model_container(self, obj):
        return obj.model_container
    format_model_container.short_description = format_html('Model<br>Container')
    format_model_container.admin_order_field = 'model_container'

    def format_tip_container(self, obj):
        return obj.tip_container
    format_tip_container.short_description = format_html('Tip<br>Container')
    format_tip_container.admin_order_field = 'tip_container'

    def format_numar_colete(self, obj):
        return obj.numar_colete
    format_numar_colete.short_description = format_html('Numar<br>Colete')
    format_numar_colete.admin_order_field = 'numar_colete'

    def format_greutate_bruta(self, obj):
        return obj.greutate_bruta
    format_greutate_bruta.short_description = format_html('Greutate<br>Bruta')
    format_greutate_bruta.admin_order_field = 'greutate_bruta'

    def format_descriere_marfa(self, obj):
        return obj.descriere_marfa[:50] + '...' if len(obj.descriere_marfa or '') > 50 else obj.descriere_marfa
    format_descriere_marfa.short_description = format_html('Descriere<br>Marfa')
    format_descriere_marfa.admin_order_field = 'descriere_marfa'

    def format_tip_operatiune(self, obj):
        return obj.tip_operatiune
    format_tip_operatiune.short_description = format_html('Tip<br>Operatiune')
    format_tip_operatiune.admin_order_field = 'tip_operatiune'

    def format_nume_nava(self, obj):
        return obj.nume_nava
    format_nume_nava.short_description = format_html('Nume<br>Nava')
    format_nume_nava.admin_order_field = 'nume_nava'

    def format_pavilion_nava(self, obj):
        return obj.pavilion_nava
    format_pavilion_nava.short_description = format_html('Pavilion<br>Nava')
    format_pavilion_nava.admin_order_field = 'pavilion_nava'

    def format_numar_sumara(self, obj):
        return obj.numar_sumara
    format_numar_sumara.short_description = format_html('Numar<br>Sumara')
    format_numar_sumara.admin_order_field = 'numar_sumara'

    def format_linie_maritima(self, obj):
        return obj.linie_maritima
    format_linie_maritima.short_description = format_html('Linie<br>Maritima')
    format_linie_maritima.admin_order_field = 'linie_maritima'

    list_filter = [
        'data_inregistrare', 'numar_manifest', 'linie_maritima'
    ]

    search_fields = [
        'numar_manifest', 'container', 'model_container', 'nume_nava',
        'numar_permis', 'descriere_marfa', 'linie_maritima'
    ]

    readonly_fields = ['numar_curent', 'model_container', 'created_at', 'updated_at']

    fieldsets = (
        ('Informatii Principale', {
            'fields': ('numar_curent', 'numar_manifest', 'numar_permis', 'numar_pozitie', 'cerere_operatiune', 'data_inregistrare')
        }),
        ('Container', {
            'fields': ('container', 'tip_container', 'model_container', 'numar_colete', 'greutate_bruta')
        }),
        ('Marfa', {
            'fields': ('descriere_marfa', 'tip_operatiune')
        }),
        ('Nava', {
            'fields': ('nume_nava', 'pavilion_nava', 'numar_sumara', 'linie_maritima')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    date_hierarchy = 'data_inregistrare'
    list_per_page = 50


# Admin pentru DatabaseYear
@admin.register(DatabaseYear)
class DatabaseYearAdmin(admin.ModelAdmin):
    """Admin pentru gestionarea bazelor de date pe ani"""
    list_display = ['year', 'is_active', 'entries_count', 'created_at']
    list_filter = ['is_active', 'year']
    search_fields = ['year']
    actions = ['activate_year']

    def entries_count(self, obj):
        return obj.entries.count()
    entries_count.short_description = 'Numar Intrari'

    def activate_year(self, request, queryset):
        # Dezactiveaza toate
        DatabaseYear.objects.all().update(is_active=False)
        # Activeaza selectiile
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} an(i) activat(i) cu succes.')
    activate_year.short_description = 'Activeaza anul selectat'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-new-year/', self.admin_site.admin_view(self.create_new_year_view), name='create_new_year'),
        ]
        return custom_urls + urls

    def create_new_year_view(self, request):
        """View pentru crearea unui an nou"""
        if request.method == 'POST':
            year = request.POST.get('year')
            try:
                year = int(year)
                # Verifica daca exista deja
                if DatabaseYear.objects.filter(year=year).exists():
                    messages.error(request, f'Anul {year} exista deja in baza de date.')
                else:
                    # Creaza anul nou
                    new_year = DatabaseYear.objects.create(year=year, is_active=False)
                    messages.success(request, f'Anul {year} a fost creat cu succes! Poti acum importa date pentru acest an.')
                return redirect('..')
            except ValueError:
                messages.error(request, 'Anul trebuie sa fie un numar valid.')
                return redirect('..')

        # GET request - afiseaza formular
        from django.template.response import TemplateResponse
        context = {
            **self.admin_site.each_context(request),
            'title': 'Creare An Nou',
            'current_year': datetime.now().year,
            'next_year': datetime.now().year + 1,
        }
        return TemplateResponse(request, 'admin/create_new_year.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_create_year_button'] = True
        return super().changelist_view(request, extra_context=extra_context)


# Admin pentru Pavilion
@admin.register(Pavilion)
class PavilionAdmin(admin.ModelAdmin):
    """Admin pentru pavilioane"""
    list_display = ['nume', 'nume_tara', 'preview_imagine', 'ships_count', 'created_at']
    search_fields = ['nume', 'nume_tara']
    readonly_fields = ['preview_imagine_large', 'created_at', 'updated_at']

    fieldsets = (
        ('Informatii Pavilion', {
            'fields': ('nume', 'nume_tara', 'imagine', 'preview_imagine_large')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def preview_imagine(self, obj):
        if obj.imagine:
            return format_html('<img src="{}" width="50" height="30" style="object-fit: contain;" />', obj.imagine.url)
        return '-'
    preview_imagine.short_description = 'Preview'

    def preview_imagine_large(self, obj):
        if obj.imagine:
            return format_html('<img src="{}" width="200" style="object-fit: contain;" />', obj.imagine.url)
        return '-'
    preview_imagine_large.short_description = 'Preview Imagine'

    def ships_count(self, obj):
        return obj.ships.count()
    ships_count.short_description = 'Numar Nave'


# Admin pentru Ship
@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    """Admin pentru nave"""
    list_display = ['nume', 'linie_maritima', 'pavilion', 'preview_imagine', 'preview_pavilion', 'entries_count', 'created_at']
    list_filter = ['linie_maritima', 'pavilion']
    search_fields = ['nume', 'linie_maritima']
    readonly_fields = ['preview_imagine_large', 'created_at', 'updated_at']
    autocomplete_fields = ['pavilion']

    fieldsets = (
        ('Informatii Nava', {
            'fields': ('nume', 'linie_maritima', 'pavilion', 'imagine', 'preview_imagine_large', 'descriere')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def preview_imagine(self, obj):
        if obj.imagine:
            return format_html('<img src="{}" width="60" height="40" style="object-fit: cover; border-radius: 4px;" />', obj.imagine.url)
        return '-'
    preview_imagine.short_description = 'Nava'

    def preview_imagine_large(self, obj):
        if obj.imagine:
            return format_html('<img src="{}" width="300" style="object-fit: contain;" />', obj.imagine.url)
        return '-'
    preview_imagine_large.short_description = 'Preview Imagine'

    def preview_pavilion(self, obj):
        if obj.pavilion and obj.pavilion.imagine:
            return format_html('<img src="{}" width="50" height="30" style="object-fit: contain;" />', obj.pavilion.imagine.url)
        return '-'
    preview_pavilion.short_description = 'Pavilion'

    def entries_count(self, obj):
        return obj.entries.count()
    entries_count.short_description = 'Intrari'


# Admin pentru ContainerType
@admin.register(ContainerType)
class ContainerTypeAdmin(admin.ModelAdmin):
    """Admin pentru tipuri containere cu extragere automata din ManifestEntry"""
    list_display = ['model_container', 'tip_container', 'preview_imagine', 'entries_count', 'created_at']
    search_fields = ['model_container', 'tip_container']
    readonly_fields = ['preview_imagine_large', 'created_at', 'updated_at']
    actions = ['extract_unique_containers']

    fieldsets = (
        ('Informatii Container', {
            'fields': ('model_container', 'tip_container', 'imagine', 'preview_imagine_large', 'descriere')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def preview_imagine(self, obj):
        if obj.imagine:
            return format_html('<img src="{}" width="60" height="40" style="object-fit: cover; border-radius: 4px;" />', obj.imagine.url)
        return '-'
    preview_imagine.short_description = 'Preview'

    def preview_imagine_large(self, obj):
        if obj.imagine:
            return format_html('<img src="{}" width="300" style="object-fit: contain;" />', obj.imagine.url)
        return '-'
    preview_imagine_large.short_description = 'Preview Imagine'

    def entries_count(self, obj):
        return obj.entries.count()
    entries_count.short_description = 'Intrari'

    def extract_unique_containers(self, request, queryset):
        """Extrage automat model_container unice din ManifestEntry si le adauga in ContainerType"""
        unique_containers = ManifestEntry.objects.exclude(model_container='').values('model_container', 'tip_container').distinct()

        created_count = 0
        for item in unique_containers:
            model = item['model_container']
            tip = item['tip_container'] or ''
            if model:
                container_type, created = ContainerType.objects.get_or_create(
                    model_container=model,
                    defaults={'tip_container': tip}
                )
                if created:
                    created_count += 1

        self.message_user(request, f'{created_count} tipuri de containere noi au fost create automat.')
    extract_unique_containers.short_description = 'Extrage containere unice din manifeste'


# Customizare User Admin pentru renumire campuri
class CustomUserAdmin(BaseUserAdmin):
    """Admin personalizat pentru utilizatori cu campuri redenumite"""

    # Customizam fieldsets pentru a redenumi campurile
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informații personale', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisiuni', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Date importante', {'fields': ('last_login', 'date_joined')}),
    )

    # Customizam list_display pentru renumirea campurilor
    list_display = ('username', 'email', 'get_full_name_custom', 'get_company_name', 'is_staff')

    def get_full_name_custom(self, obj):
        """Afiseaza first_name ca 'Nume si prenume'"""
        return obj.first_name or '-'
    get_full_name_custom.short_description = 'Nume si prenume'

    def get_company_name(self, obj):
        """Afiseaza last_name ca 'Nume companie'"""
        return obj.last_name or '-'
    get_company_name.short_description = 'Nume companie'

    # Suprascriu get_form pentru a customiza label-urile campurilor
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'first_name' in form.base_fields:
            form.base_fields['first_name'].label = 'Nume si prenume'
        if 'last_name' in form.base_fields:
            form.base_fields['last_name'].label = 'Nume companie'
        return form


# Inregistrare User Admin personalizat
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Customizare titluri admin
admin.site.site_header = "Registru import RE1"
admin.site.site_title = "Registru import RE1"
admin.site.index_title = "Administrare Registru Import"
