#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pentru migrarea datelor din Django SQLite în MySQL PHP
"""
import sqlite3
import json
import sys

# Path la database-ul Django
DJANGO_DB = r'C:\Users\Laurentiu\Desktop\Proiect RE1\db.sqlite3'

def export_data():
    """Exportă datele din Django SQLite"""
    try:
        conn = sqlite3.connect(DJANGO_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        data = {
            'ships': [],
            'ports': [],
            'manifests': [],
            'manifest_entries': [],
            'countries': [],
            'container_types': []
        }

        # Export Ships
        print("Exportare nave...")
        cursor.execute("SELECT * FROM manifests_ship")
        for row in cursor.fetchall():
            data['ships'].append({
                'id': row['id'],
                'name': row['name'],
                'image': row['image']
            })
        print(f"  {len(data['ships'])} nave exportate")

        # Export Ports
        print("Exportare porturi...")
        cursor.execute("SELECT * FROM manifests_port")
        for row in cursor.fetchall():
            data['ports'].append({
                'id': row['id'],
                'name': row['name'],
                'country': row['country']
            })
        print(f"  {len(data['ports'])} porturi exportate")

        # Export Countries
        print("Exportare țări...")
        cursor.execute("SELECT * FROM manifests_country")
        for row in cursor.fetchall():
            data['countries'].append({
                'id': row['id'],
                'name': row['name'],
                'code': row['code'],
                'flag_image': row['flag_image']
            })
        print(f"  {len(data['countries'])} țări exportate")

        # Export Container Types
        print("Exportare tipuri containere...")
        cursor.execute("SELECT * FROM manifests_containertype")
        for row in cursor.fetchall():
            data['container_types'].append({
                'id': row['id'],
                'code': row['code'],
                'prefix': row['prefix'],
                'description': row['description'],
                'image': row['image']
            })
        print(f"  {len(data['container_types'])} tipuri containere exportate")

        # Export Manifests
        print("Exportare manifeste...")
        cursor.execute("SELECT * FROM manifests_manifest")
        for row in cursor.fetchall():
            data['manifests'].append({
                'id': row['id'],
                'manifest_number': row['manifest_number'],
                'ship_id': row['ship_id'],
                'arrival_date': row['arrival_date'],
                'port_id': row['port_id']
            })
        print(f"  {len(data['manifests'])} manifeste exportate")

        # Export Manifest Entries
        print("Exportare înregistrări manifest...")
        cursor.execute("SELECT * FROM manifests_manifestentry")
        for row in cursor.fetchall():
            data['manifest_entries'].append({
                'id': row['id'],
                'manifest_id': row['manifest_id'],
                'container_number': row['container_number'],
                'container_type': row['container_type'],
                'seal_number': row['seal_number'],
                'goods_description': row['goods_description'],
                'weight': row['weight'],
                'shipper': row['shipper'],
                'consignee': row['consignee'],
                'marks_numbers': row['marks_numbers'],
                'country_of_origin': row['country_of_origin'],
                'country_code': row['country_code'],
                'container_image': row['container_image']
            })
        print(f"  {len(data['manifest_entries'])} înregistrări exportate")

        conn.close()

        # Salvează în JSON
        output_file = 'django_data_export.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Date exportate cu succes în: {output_file}")
        print(f"\nTotal:")
        print(f"  - {len(data['ships'])} nave")
        print(f"  - {len(data['ports'])} porturi")
        print(f"  - {len(data['countries'])} țări")
        print(f"  - {len(data['container_types'])} tipuri containere")
        print(f"  - {len(data['manifests'])} manifeste")
        print(f"  - {len(data['manifest_entries'])} containere")

        return True

    except sqlite3.Error as e:
        print(f"✗ Eroare SQLite: {e}")
        return False
    except Exception as e:
        print(f"✗ Eroare: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("  EXPORT DATE DIN DJANGO")
    print("=" * 50)
    print()

    if export_data():
        print("\nGata! Acum rulează import_django_data.php pentru a importa în MySQL")
    else:
        sys.exit(1)
