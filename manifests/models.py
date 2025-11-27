from django.db import models
from django.core.validators import MinValueValidator


class DatabaseYear(models.Model):
    """Model pentru gestionarea bazelor de date pe ani"""
    year = models.IntegerField(unique=True, verbose_name="An")
    is_active = models.BooleanField(default=False, verbose_name="Activ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")

    class Meta:
        verbose_name = "An Baza Date"
        verbose_name_plural = "Ani Baze Date"
        ordering = ['-year']

    def __str__(self):
        return f"Registru {self.year}"


class ContainerType(models.Model):
    """Model pentru tipuri de containere cu imagini"""
    model_container = models.CharField(max_length=100, unique=True, verbose_name="Model Container")
    tip_container = models.CharField(max_length=50, verbose_name="Tip Container")
    imagine = models.ImageField(upload_to='container_types/', null=True, blank=True, verbose_name="Imagine Container")
    descriere = models.TextField(blank=True, verbose_name="Descriere")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")

    class Meta:
        verbose_name = "Tip Container"
        verbose_name_plural = "Tipuri Containere"
        ordering = ['model_container']

    def __str__(self):
        return f"{self.model_container} - {self.tip_container}"


class Pavilion(models.Model):
    """Model pentru pavilioane nave cu imagini"""
    nume = models.CharField(max_length=100, unique=True, verbose_name="Nume Pavilion")
    imagine = models.ImageField(upload_to='pavilions/', null=True, blank=True, verbose_name="Imagine Pavilion")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")

    class Meta:
        verbose_name = "Pavilion"
        verbose_name_plural = "Pavilioane"
        ordering = ['nume']

    def __str__(self):
        return self.nume


class Ship(models.Model):
    """Model pentru nave cu imagini"""
    nume = models.CharField(max_length=200, unique=True, verbose_name="Nume Nava")
    linie_maritima = models.CharField(max_length=200, blank=True, verbose_name="Linie Maritima")
    pavilion = models.ForeignKey(Pavilion, on_delete=models.SET_NULL, null=True, blank=True, related_name='ships', verbose_name="Pavilion")
    imagine = models.ImageField(upload_to='ships/', null=True, blank=True, verbose_name="Imagine Nava")
    descriere = models.TextField(blank=True, verbose_name="Descriere")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")

    class Meta:
        verbose_name = "Nava"
        verbose_name_plural = "Nave"
        ordering = ['nume']

    def __str__(self):
        return self.nume


class ManifestEntry(models.Model):
    """Model pentru intrari din manifestele de marfa"""

    # An baza de date
    database_year = models.ForeignKey(DatabaseYear, on_delete=models.CASCADE, related_name='entries', null=True, blank=True, verbose_name="An Baza Date")

    # Numar curent (generat automat)
    numar_curent = models.IntegerField(default=0, db_index=True, verbose_name="Numar Curent")

    # Coloane din Excel
    numar_manifest = models.CharField(max_length=100, db_index=True, verbose_name="Numar Manifest")
    numar_permis = models.CharField(max_length=100, blank=True, verbose_name="Numar Permis")
    numar_pozitie = models.CharField(max_length=50, blank=True, verbose_name="Numar Pozitie")
    cerere_operatiune = models.CharField(max_length=100, blank=True, verbose_name="Cerere Operatiune")
    data_inregistrare = models.DateField(null=True, blank=True, verbose_name="Data Inregistrare")
    container = models.CharField(max_length=50, db_index=True, verbose_name="Container")
    numar_colete = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], verbose_name="Numar Colete")
    greutate_bruta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Greutate Bruta (kg)")
    descriere_marfa = models.TextField(blank=True, verbose_name="Descriere Marfa")
    tip_operatiune = models.CharField(max_length=1, blank=True, verbose_name="Tip Operatiune")
    nume_nava = models.CharField(max_length=200, blank=True, verbose_name="Nume Nava")
    pavilion_nava = models.CharField(max_length=100, blank=True, verbose_name="Pavilion Nava")
    numar_sumara = models.CharField(max_length=100, blank=True, null=True, verbose_name="Numar Sumara")
    tip_container = models.CharField(max_length=50, blank=True, verbose_name="Tip Container")
    linie_maritima = models.CharField(max_length=200, blank=True, verbose_name="Linie Maritima")

    # Coloana generata automat
    model_container = models.CharField(max_length=100, blank=True, editable=False, verbose_name="Model Container")

    # Relatii cu tabelele noi
    container_type_rel = models.ForeignKey(ContainerType, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries', verbose_name="Tip Container (Relatie)")
    ship_rel = models.ForeignKey(Ship, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries', verbose_name="Nava (Relatie)")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")

    class Meta:
        verbose_name = "Intrare Registru Import"
        verbose_name_plural = "Registru Import 2025"
        ordering = ['numar_curent']
        indexes = [
            models.Index(fields=['numar_manifest', 'container']),
            models.Index(fields=['data_inregistrare']),
            models.Index(fields=['numar_curent']),
        ]

    def save(self, *args, **kwargs):
        """Override save pentru a genera automat model_container si a lega relatiile"""
        # Genereaza model_container
        if self.container and self.tip_container:
            prefix = self.container[:4] if len(self.container) >= 4 else self.container
            self.model_container = f"{prefix}{self.tip_container}"
        else:
            self.model_container = ""

        # Seteaza database_year daca nu e setat (pentru backwards compatibility)
        if not self.database_year_id:
            try:
                # Incearca sa gaseasca anul activ sau cel mai recent
                active_year = DatabaseYear.objects.filter(is_active=True).first()
                if not active_year:
                    active_year = DatabaseYear.objects.order_by('-year').first()
                if active_year:
                    self.database_year = active_year
            except DatabaseYear.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # AUTO-CREARE ContainerType daca nu exista
        if self.model_container and not self.container_type_rel:
            try:
                container_type = ContainerType.objects.get(model_container=self.model_container)
                self.container_type_rel = container_type
                super().save(update_fields=['container_type_rel'])
            except ContainerType.DoesNotExist:
                # Creeaza automat ContainerType nou
                container_type = ContainerType.objects.create(
                    model_container=self.model_container,
                    tip_container=self.tip_container or ''
                )
                self.container_type_rel = container_type
                super().save(update_fields=['container_type_rel'])

        # AUTO-CREARE Pavilion si Ship daca nu exista
        if self.nume_nava and not self.ship_rel:
            # Mai intai verifica/creeaza Pavilion
            pavilion_obj = None
            if self.pavilion_nava:
                pavilion_obj, _ = Pavilion.objects.get_or_create(
                    nume=self.pavilion_nava.strip()
                )

            # Apoi verifica/creeaza Ship
            try:
                ship = Ship.objects.get(nume__iexact=self.nume_nava)
                self.ship_rel = ship
                super().save(update_fields=['ship_rel'])
            except Ship.DoesNotExist:
                # Creeaza automat Ship nou
                ship = Ship.objects.create(
                    nume=self.nume_nava.strip(),
                    linie_maritima=self.linie_maritima or '',
                    pavilion=pavilion_obj
                )
                self.ship_rel = ship
                super().save(update_fields=['ship_rel'])

    def __str__(self):
        return f"{self.numar_manifest} - {self.container}"
