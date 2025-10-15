turno = 1  # 1 para proceso1, 2 para proceso2
import curses
import threading
import time

# Variables globales
proceso1_esta_dentro = False
proceso2_esta_dentro = False
turno = 1  # 1 para proceso1, 2 para proceso2
cancelar = False

# Ventanas
winA = None
winB = None
winTop = None
winBottom = None


# --- Funciones auxiliares ---
def retardar_unos_milisegundos(ms):
    """Simula retardo para que la animación sea visible."""
    for _ in range(ms):
        if cancelar:
            break
        pass


def ejecutar_seccion_critica_1():
    """Acción visual del proceso 1."""
    winA.addstr("+")
    winA.refresh()
    retardar_unos_milisegundos(2000)


def ejecutar_seccion_critica_2():
    """Acción visual del proceso 2."""
    winB.addstr("*")
    winB.refresh()
    retardar_unos_milisegundos(2000)


def proceso1():
    global proceso1_esta_dentro, proceso2_esta_dentro, turno, cancelar

    while not cancelar:
        # Intenta entrar en la sección crítica
        proceso1_esta_dentro = True
        while proceso2_esta_dentro:
            if turno == 2:
                proceso1_esta_dentro = False
                while turno == 2 and not cancelar:
                    pass  # Esperar turno
                proceso1_esta_dentro = True

        # --- Sección crítica ---
        if cancelar:
            break
        ejecutar_seccion_critica_1()

        # --- Salida de la sección crítica ---
        turno = 2
        proceso1_esta_dentro = False

        retardar_unos_milisegundos(1000)  # Simula trabajo fuera de SC

    winA.addstr("\nHa terminado el proceso 1\n")
    winA.refresh()


def proceso2():
    global proceso1_esta_dentro, proceso2_esta_dentro, turno, cancelar

    while not cancelar:
        # Intenta entrar en la sección crítica
        proceso2_esta_dentro = True
        while proceso1_esta_dentro:
            if turno == 1:
                proceso2_esta_dentro = False
                while turno == 1 and not cancelar:
                    pass  # Esperar turno
                proceso2_esta_dentro = True

        # --- Sección crítica ---
        if cancelar:
            break
        ejecutar_seccion_critica_2()

        # --- Salida de la sección crítica ---
        turno = 1
        proceso2_esta_dentro = False

        retardar_unos_milisegundos(1000)

    winB.addstr("\nHa terminado el proceso 2\n")
    winB.refresh()


# --- Interfaz con curses ---
def inicializar_pantallas(stdscr):
    global winA, winB, winTop, winBottom

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    h, w = stdscr.getmaxyx()

    winA = curses.newwin(h - 2, (w // 2) - 1, 1, 0)
    winB = curses.newwin(h - 2, (w // 2) - 1, 1, (w // 2))
    winTop = curses.newwin(1, w, 0, 0)
    winBottom = curses.newwin(1, w, h - 1, 0)

    titulo = "=== Algoritmo de Dekker III ==="
    winTop.addstr(0, (w // 2) - len(titulo) // 2, titulo)
    winTop.refresh()

    winBottom.addstr(0, 0, "Presione [Enter] para salir.")
    winBottom.refresh()


def main(stdscr):
    global cancelar

    inicializar_pantallas(stdscr)

    cancelar = False

    # Crear hilos
    t1 = threading.Thread(target=proceso1)
    t2 = threading.Thread(target=proceso2)

    t1.start()
    t2.start()

    # Esperar a que el usuario presione Enter
    stdscr.getch()
    cancelar = True

    t1.join()
    t2.join()

    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)
