import os

def merge_all_ics_in_folder(output_filename):
    # Liste tous les fichiers .ics dans le répertoire actuel, sauf le fichier de sortie s'il existe déjà
    ics_files = [f for f in os.listdir('.') if f.endswith('.ics') and f != output_filename]
    
    if not ics_files:
        print("Aucun fichier .ics trouvé dans le dossier.")
        return

    combined_content = []
    header_extracted = False

    for filename in ics_files:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # Pour le premier fichier, on récupère l'entête (PRODID, TIMEZONE, etc.)
            if not header_extracted:
                for line in lines:
                    if "BEGIN:VEVENT" in line:
                        header_extracted = True
                        combined_content.append(line)
                    elif "END:VCALENDAR" not in line:
                        combined_content.append(line)
            else:
                # Pour les fichiers suivants, on ne prend que les blocs VEVENT
                is_inside_vevent = False
                for line in lines:
                    if "BEGIN:VEVENT" in line:
                        is_inside_vevent = True
                    
                    if is_inside_vevent:
                        if "END:VCALENDAR" not in line:
                            combined_content.append(line)
                        if "END:VEVENT" in line:
                            is_inside_vevent = False

    # On s'assure que le fichier se termine correctement
    if not combined_content[-1].strip() == "END:VCALENDAR":
        combined_content.append("END:VCALENDAR\n")

    # Écriture du fichier final
    with open(output_filename, 'w', encoding='utf-8') as out:
        out.writelines(combined_content)
    
    print(f"Fusion terminée ! {len(ics_files)} fichiers assemblés dans '{output_filename}'.")

# Exécution
merge_all_ics_in_folder('Calendrier_Global_Fusionne.ics')