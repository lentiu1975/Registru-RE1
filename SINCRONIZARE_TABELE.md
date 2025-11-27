# Sincronizare Automată Tabele de Referință

## Descriere

Sistemul sincronizează automat tabelele `ContainerType`, `Ship` și `Pavilion` cu valorile din `ManifestEntry`.

## Funcționare Automată

### La Salvarea Fiecărei Intrări ManifestEntry

Când salvezi o intrare nouă în `ManifestEntry`, sistemul automat:

1. **Creează ContainerType** dacă `model_container` nu există în tabelă
   - Folosește valorile din `container` + `tip_container`
   - Generează automat `model_container` (primele 4 caractere + tip)

2. **Creează Pavilion** dacă `pavilion_nava` nu există în tabelă
   - Folosește valoarea din coloana `pavilion nava`

3. **Creează Ship** dacă `nume_nava` nu există în tabelă
   - Folosește valorile din `nume nava`, `linie maritima` și `pavilion nava`
   - Leagă automat nava de pavilion

4. **Actualizează Relațiile** în ManifestEntry
   - Setează `container_type_rel` la ContainerType corespunzător
   - Setează `ship_rel` la Ship corespunzător

## Sincronizare Manuală

### Metoda 1: Command Line

Rulează command-ul Django pentru a sincroniza toate intrările existente:

```bash
py manage.py sync_lookup_tables
```

Acest command:
- Extrage toate valorile unice din ManifestEntry
- Creează înregistrări noi în ContainerType, Ship și Pavilion
- Actualizează toate relațiile în ManifestEntry

### Metoda 2: Admin Interface

1. Accesează interfața admin: `http://localhost:8000/admin/`
2. Mergi la secțiunea **Registru Import 2025**
3. Selectează orice intrări (sau niciuna)
4. Din dropdown-ul "Actions", alege **"Sincronizeaza tabele (ContainerType, Ship, Pavilion)"**
5. Click pe **"Go"**

## Import Date din Excel

După ce importi date noi din Excel:

1. **Sincronizare Automată**: Fiecare intrare nouă va crea automat înregistrări în tabelele de referință
2. **Sincronizare Manuală** (opțional): Rulează `py manage.py sync_lookup_tables` pentru a actualiza toate relațiile

## Adăugare Imagini

După sincronizare, poți adăuga imagini pentru:

1. **Tipuri Containere**: Mergi la admin → Tipuri Containere → selectează un tip → încarcă imagine
2. **Nave**: Mergi la admin → Nave → selectează o navă → încarcă imagine
3. **Pavilioane**: Mergi la admin → Pavilioane → selectează un pavilion → încarcă steag

Imaginile vor apărea automat în interfața de căutare pentru utilizatori.

## Structura Datelor

### ManifestEntry (Tabel Principal)
- `container` + `tip_container` → generează `model_container`
- `nume_nava`, `linie_maritima`, `pavilion_nava` → date pentru Ship
- `pavilion_nava` → date pentru Pavilion

### Tabele de Referință (Auto-populate)
- **ContainerType**: Modele unice de containere cu imagini
- **Pavilion**: Pavilioane/steaguri unice cu imagini
- **Ship**: Nave unice cu imagini, legate de pavilion

## Exemplu Workflow

1. **Importă Excel** cu date noi
   - Sistem creează automat 50 containere noi în ContainerType
   - Sistem creează automat 10 nave noi în Ship
   - Sistem creează automat 3 pavilioane noi în Pavilion

2. **Adaugă Imagini** (optional)
   - Mergi în admin și adaugă poze pentru containerele/navele/pavilionele noi

3. **Utilizatorii Caută**
   - Utilizatorii văd automat imaginile când caută containere
   - Toate relațiile sunt deja create automat

## Notă Importantă

**Nu trebuie să mai gestionezi manual tabelele de referință!**
Sistemul face totul automat la import/salvare.
