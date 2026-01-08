import sys
from ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication, QStyleFactory

def main():
    app = QApplication(sys.argv)

    app.setStyle(QStyleFactory.create("Fusion"))

    # 🔑 IDENTITÉ DE L’APP (OBLIGATOIRE POUR WAYLAND)
    app.setApplicationName("MagicTable")
    app.setDesktopFileName("MagicTable")

    # Charger le thème
    app.setStyleSheet(load_qss(
        "styles/dark_green_dashboard.qss",
        "styles/dark_green_tournament.qss",
        "styles/dark_green_player.qss",
        "styles/dark_green_matche.qss",
        "styles/dark_green_setting.qss",
        "styles/dark_green_main.qss",
        "styles/dark_green_widget.qss",
    ))

    """app.setStyleSheet(load_qss("styles/dark_green_widget.qss"))"""
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

def load_qss(*paths):
    css = ""
    for path in paths:
        with open(path, "r") as f:
            css += f.read() + "\n"
    return css

if __name__ == "__main__":
    main()

app = QApplication(sys.argv)

# 🔑 CRUCIAL POUR LINUX + QSS
app.setStyle(QStyleFactory.create("Fusion"))
