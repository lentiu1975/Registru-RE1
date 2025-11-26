from django.db import models
from django.core.validators import MinValueValidator


class ManifestEntry(models.Model):
    """Model pentru intrari din manifestele de marfa"""

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
        """Override save pentru a genera automat model_container"""
        if self.container and self.tip_container:
            # Concatenare primele 4 caractere din container + tip_container
            prefix = self.container[:4] if len(self.container) >= 4 else self.container
            self.model_container = f"{prefix}{self.tip_container}"
        else:
            self.model_container = ""

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numar_manifest} - {self.container}"
