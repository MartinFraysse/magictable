import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # 🔑 IDENTITÉ DE L’APP (OBLIGATOIRE POUR WAYLAND)
    app.setApplicationName("MagicTable")
    app.setDesktopFileName("MagicTable")

    # Charger le thème
    with open("styles/dark_green.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
