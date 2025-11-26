from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import ManifestEntry
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


@admin.register(ManifestEntry)
class ManifestEntryAdmin(ImportExportModelAdmin):
    """Admin pentru ManifestEntry cu import/export Excel"""

    resource_class = ManifestEntryResource

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


# Customizare titluri admin
admin.site.site_header = "Registru Import 2025"
admin.site.site_title = "Registru Import 2025"
admin.site.index_title = "Administrare Registru Import"
