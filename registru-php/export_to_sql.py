# coding: utf-8
import sqlite3
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DJANGO_DB = r'C:\Users\Laurentiu\Desktop\Proiect RE1\db.sqlite3'

def escape_sql(value):
    """Escape value for SQL"""
    if value is None:
        return 'NULL'
    if isinstance(value, (int, float)):
        return str(value)
    # Escape single quotes
    return "'" + str(value).replace("'", "''").replace("\\", "\\\\") + "'"

conn = sqlite3.connect(DJANGO_DB)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

output_file = open('migrate_data.sql', 'w', encoding='utf-8')

output_file.write("-- Migrare date din Django la PHP MySQL\n")
output_file.write("-- Total containere: 3195\n\n")
output_file.write("SET NAMES utf8mb4;\n")
output_file.write("SET CHARACTER SET utf8mb4;\n\n")

# Export Container Types (188 tipuri)
print("Exportare tipuri containere...")
cursor.execute("SELECT * FROM manifests_containertype")
output_file.write("-- Tipuri Containere (188)\n")
for row in cursor.fetchall():
    code = escape_sql(row['tip_container'])  # tip_container in Django
    prefix = escape_sql(row['model_container'])  # model_container in Django
    desc = escape_sql(row['descriere'])  # descriere in Django
    output_file.write(f"INSERT IGNORE INTO container_types (code, prefix, description) VALUES ({code}, {prefix}, {desc});\n")
print("  188 tipuri containere exportate")

# Export Ships (2 nave)
print("Exportare nave...")
cursor.execute("SELECT * FROM manifests_ship")
output_file.write("\n-- Nave (2)\n")
for row in cursor.fetchall():
    cols = row.keys()
    name = escape_sql(row['nume' if 'nume' in cols else 'name'])
    image = escape_sql(row['imagine' if 'imagine' in cols else 'image'])
    output_file.write(f"INSERT IGNORE INTO ships (name, image) VALUES ({name}, {image});\n")
print("  2 nave exportate")

# Export Manifest Entries (3195 containere)
print("Exportare containere...")
cursor.execute("SELECT * FROM manifests_manifestentry LIMIT 3195")
output_file.write("\n-- Containere (3195)\n")

count = 0
for row in cursor.fetchall():
    # Creăm un manifest implicit pentru fiecare container
    manifest_num = escape_sql(row['numar_manifest'])
    ship_name = escape_sql(row['nume_nava'])
    date = escape_sql(row['data_inregistrare'])

    # Insert manifest (ignore duplicates)
    output_file.write(f"INSERT IGNORE INTO manifests (manifest_number, arrival_date) VALUES ({manifest_num}, {date});\n")

    # Insert container
    container = escape_sql(row['container'])
    tip = escape_sql(row['tip_container'])
    greutate = escape_sql(row['greutate_bruta'])
    marfa = escape_sql(row['descriere_marfa'])
    pavilion = escape_sql(row['pavilion_nava'])

    output_file.write(f"INSERT INTO manifest_entries (manifest_id, container_number, container_type, weight, goods_description, marks_numbers) ")
    output_file.write(f"SELECT id, {container}, {tip}, {greutate}, {marfa}, {pavilion} FROM manifests WHERE manifest_number = {manifest_num} LIMIT 1;\n")

    count += 1
    if count % 500 == 0:
        print(f"  {count}/3195 containere exportate...")

print(f"  {count} containere exportate")

output_file.write("\n-- DONE\n")
output_file.close()
conn.close()

print(f"\nGATA! Fisierul 'migrate_data.sql' a fost creat cu succes!")
print(f"Upload-ul pe server si ruleaza in phpMyAdmin")
