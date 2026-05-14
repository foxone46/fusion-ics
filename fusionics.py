import curses
import os

OUTPUT_FILENAME = 'Calendrier_Global_Fusionne.ics'


def select_files(stdscr, ics_files):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    selected = [False] * len(ics_files)
    current = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(0, 0, "Sélectionnez les calendriers à fusionner :", curses.A_BOLD)
        stdscr.addstr(1, 0, "  ↑↓ naviguer   Espace sélectionner   Entrée confirmer   q quitter")

        for i, filename in enumerate(ics_files):
            y = i + 3
            if y >= h - 1:
                break
            checkbox = "[X]" if selected[i] else "[ ]"
            line = f"  {checkbox} {filename}"
            if i == current:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, 0, line[:w - 1])
                stdscr.attroff(curses.color_pair(1))
            else:
                if selected[i]:
                    stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, 0, line[:w - 1])
                if selected[i]:
                    stdscr.attroff(curses.color_pair(2))

        count = sum(selected)
        stdscr.addstr(h - 1, 0, f"  {count} fichier(s) sélectionné(s)")

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')) and current > 0:
            current -= 1
        elif key in (curses.KEY_DOWN, ord('j')) and current < len(ics_files) - 1:
            current += 1
        elif key == ord(' '):
            selected[current] = not selected[current]
        elif key in (curses.KEY_ENTER, ord('\n'), ord('\r')):
            return [ics_files[i] for i, s in enumerate(selected) if s]
        elif key == ord('q'):
            return None


def merge_ics(ics_files):
    combined_content = []
    header_extracted = False

    for filename in ics_files:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not header_extracted:
            for line in lines:
                if "BEGIN:VEVENT" in line:
                    header_extracted = True
                    combined_content.append(line)
                elif "END:VCALENDAR" not in line:
                    combined_content.append(line)
        else:
            inside = False
            for line in lines:
                if "BEGIN:VEVENT" in line:
                    inside = True
                if inside:
                    if "END:VCALENDAR" not in line:
                        combined_content.append(line)
                    if "END:VEVENT" in line:
                        inside = False

    if not combined_content:
        return False

    if combined_content[-1].strip() != "END:VCALENDAR":
        combined_content.append("END:VCALENDAR\n")

    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as out:
        out.writelines(combined_content)

    return True


def main():
    ics_files = sorted(
        f for f in os.listdir('.')
        if f.endswith('.ics') and f != OUTPUT_FILENAME
    )

    if not ics_files:
        print("Aucun fichier .ics trouvé dans le dossier.")
        return

    chosen = curses.wrapper(select_files, ics_files)

    if chosen is None:
        print("Annulé.")
        return

    if not chosen:
        print("Aucun fichier sélectionné.")
        return

    if merge_ics(chosen):
        print(f"Fusion terminée ! {len(chosen)} fichier(s) assemblé(s) dans '{OUTPUT_FILENAME}'.")
    else:
        print("Erreur : aucun contenu à fusionner.")


if __name__ == '__main__':
    main()
