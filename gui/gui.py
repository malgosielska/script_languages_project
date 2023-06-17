import sys

from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QColor, QPalette, QPixmap)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout,
                               QPushButton, QVBoxLayout, QWidget, QStyleFactory, QMainWindow, QLabel, QListWidget,
                               QCheckBox, QScrollArea)

# from database_handler.recipe_generator import generate_recipes
from database_handler.utils import get_ingredients_names, get_recipes_names


# from gui.gui_handler import handle_checkbox


class MainWindow(QMainWindow):

    def __init__(self, ingredients, recipes):
        super().__init__()

        self.ingredients = ingredients
        self.recipes = recipes

        self.setWindowTitle("Recipe Generator")
        self.setMinimumWidth(1000)

        # Dodaję centralny widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Tworzę horyzontalny main_layout
        self.main_layout = QHBoxLayout(self.central_widget)

        # Tworzę wertykalny left_layout i dodaję do main_layout
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

        # Dodaję miejsce na zdjęcie w lewym górnym rogu
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap("pink_lady.jpg").scaledToWidth(100))
        self.image_label.setFixedSize(100, 100)
        self.left_layout.addWidget(self.image_label)

        self.ingrediens_label = QLabel("SELECT INGREDIENTS")
        self.ingrediens_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingrediens_label.setStyleSheet("color: black;font-weight: bold;")
        self.ingrediens_label.setFixedSize(400, 30)  # Ustawienie szerokości na 400 pikseli i wysokości na 30 pikseli
        self.left_layout.addWidget(self.ingrediens_label)

        self.selected_ingrediens = []
        self.checkboxes_list = []
        # Wyświetlanie elementów listy składników

        self.checkboxes_widget = QWidget()
        self.checkboxes_layout = QVBoxLayout()
        self.checkboxes_widget.setLayout(self.checkboxes_layout)

        for ingredient in ingredients:
            # Tworzę QCheckBox
            self.checkbox = QCheckBox(ingredient)
            self.checkbox.setStyleSheet("color: black; QCheckBox: white;")
            self.checkbox.setChecked(False)  # Domyślnie zaznaczony
            self.checkboxes_list.append(self.checkbox)
            self.checkboxes_layout.addWidget(self.checkbox)
            # self.selected_ingrediens.append(ingredient)

        # self.left_layout.addWidget(self.checkboxes_widget)

        self.scroll_area = QScrollArea()
        # self.scroll_area.setFixedSize(400, 100)
        self.scroll_area.setWidgetResizable(True)

        # Ustawianie kontenera jako wewnętrznego widżetu kontenera przewijania
        self.scroll_area.setWidget(self.checkboxes_widget)

        # Dodawanie kontenera przewijania do głównego okna
        # self.set(scroll_area)
        self.left_layout.addWidget(self.scroll_area)

        # Tworzę wertykalny right_layout
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout)

        # Przycisk "Generate Recipes" na samej górze
        self.button = QPushButton("Generate Recipes")
        self.button.clicked.connect(self.generate_recipes)
        self.right_layout.addWidget(self.button, alignment=Qt.AlignTop)

        self.recipes_list = QListWidget()
        list_palette = self.recipes_list.palette()
        list_palette.setColor(QPalette.ColorRole.Base, Qt.white)
        self.recipes_list.setPalette(list_palette)
        self.right_layout.addWidget(self.recipes_list)

    def handle_checkbox(self):

        selected_ingredients = []
        for checkbox in self.checkboxes_list:
            # checkbox = app.sender()
            ingredient = checkbox.text()

            if checkbox.isChecked():
                selected_ingredients.append(ingredient)
        return selected_ingredients

    def generate_recipes(self):
        self.selected_ingrediens = self.handle_checkbox()
        # print(self.handle_checkbox)
        print("Selected Ingredients:", self.selected_ingrediens)
        # # Wyświetlanie przepisów po kliknięciu przycisku
        self.recipes_list.clear()
        # matching_recipes = [recipe for recipe in gui.recipes if
        #                     all(ingredient in gui.selected_ingredients for ingredient in
        #                         recipe["specific_ingredients"])]
        # if matching_recipes:
        #     for recipe in matching_recipes:
        #         gui.recipes_list.addItem(recipe["recipe_title"])
        # else:
        self.recipes_list.addItem("No recipes found")
        # gui.recipes_list.addItems(gui.recipes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle(QStyleFactory.create("Fusion"))
    pink_palette = QPalette()
    pink_palette.setColor(QPalette.ColorRole.Window, QColor(255, 228, 225))
    pink_palette.setColor(QPalette.ColorRole.Text, QColor(128, 0, 0))
    pink_palette.setColor(QPalette.ColorRole.Button, QColor(255, 105, 180))
    pink_palette.setColor(QPalette.ColorRole.ButtonText, QColor(128, 0, 0))
    pink_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    pink_palette.setColor(QPalette.ColorRole.Link, QColor(255, 20, 147))
    pink_palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 20, 147))
    pink_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(128, 0, 0))

    app.setPalette(pink_palette)

    # todo wczytywanie danych z bazy
    ingredients = get_ingredients_names()
    recipes = get_recipes_names()

    dialog = QDialog()
    ui = MainWindow(ingredients, recipes)
    ui.show()
    sys.exit(app.exec())
