"""
Management command pentru sincronizarea automata a tabelelor de referinta
(ContainerType, Ship, Pavilion) cu valorile din ManifestEntry
"""
from django.core.management.base import BaseCommand
from django.db import models
from manifests.models import ManifestEntry, ContainerType, Ship, Pavilion


class Command(BaseCommand):
    help = 'Sincronizeaza automat tabelele ContainerType, Ship si Pavilion cu valorile din ManifestEntry'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Incep sincronizarea tabelelor de referinta...'))

        # 1. Sincronizeaza ContainerType
        self.stdout.write('\n1. Sincronizare ContainerType...')
        unique_containers = ManifestEntry.objects.exclude(
            model_container=''
        ).values('model_container', 'tip_container').distinct()

        container_created = 0
        for item in unique_containers:
            model = item['model_container']
            tip = item['tip_container'] or ''
            if model:
                _, created = ContainerType.objects.get_or_create(
                    model_container=model,
                    defaults={'tip_container': tip}
                )
                if created:
                    container_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'   > {container_created} tipuri de containere noi create'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'   > Total ContainerType: {ContainerType.objects.count()}'
        ))

        # 2. Sincronizeaza Pavilion
        self.stdout.write('\n2. Sincronizare Pavilion...')
        unique_pavilions = ManifestEntry.objects.exclude(
            pavilion_nava=''
        ).values_list('pavilion_nava', flat=True).distinct()

        pavilion_created = 0
        for pavilion_name in unique_pavilions:
            if pavilion_name and pavilion_name.strip():
                _, created = Pavilion.objects.get_or_create(
                    nume=pavilion_name.strip()
                )
                if created:
                    pavilion_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'   > {pavilion_created} pavilioane noi create'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'   > Total Pavilion: {Pavilion.objects.count()}'
        ))

        # 3. Sincronizeaza Ship
        self.stdout.write('\n3. Sincronizare Ship...')
        unique_ships = ManifestEntry.objects.exclude(
            nume_nava=''
        ).values('nume_nava', 'linie_maritima', 'pavilion_nava').distinct()

        ship_created = 0
        for item in unique_ships:
            nume = item['nume_nava']
            if nume and nume.strip():
                # Gaseste pavilion daca exista
                pavilion_obj = None
                if item['pavilion_nava']:
                    try:
                        pavilion_obj = Pavilion.objects.get(nume=item['pavilion_nava'].strip())
                    except Pavilion.DoesNotExist:
                        pass

                _, created = Ship.objects.get_or_create(
                    nume=nume.strip(),
                    defaults={
                        'linie_maritima': item['linie_maritima'] or '',
                        'pavilion': pavilion_obj
                    }
                )
                if created:
                    ship_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'   > {ship_created} nave noi create'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'   > Total Ship: {Ship.objects.count()}'
        ))

        # 4. Actualizeaza relatiile in ManifestEntry
        self.stdout.write('\n4. Actualizare relatii in ManifestEntry...')

        entries_updated = 0
        entries_to_update = ManifestEntry.objects.filter(
            models.Q(container_type_rel__isnull=True) | models.Q(ship_rel__isnull=True)
        )

        for entry in entries_to_update:
            updated = False

            # Leaga ContainerType
            if entry.model_container and not entry.container_type_rel:
                try:
                    container_type = ContainerType.objects.get(model_container=entry.model_container)
                    entry.container_type_rel = container_type
                    updated = True
                except ContainerType.DoesNotExist:
                    pass

            # Leaga Ship
            if entry.nume_nava and not entry.ship_rel:
                try:
                    ship = Ship.objects.get(nume__iexact=entry.nume_nava)
                    entry.ship_rel = ship
                    updated = True
                except Ship.DoesNotExist:
                    pass

            if updated:
                entry.save()
                entries_updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'   > {entries_updated} intrari ManifestEntry actualizate cu relatii'
        ))

        self.stdout.write(self.style.SUCCESS(
            f'\n> Sincronizare completa!'
        ))
