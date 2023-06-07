import sys

from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QColor, QPalette, QPixmap)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout,
                               QPushButton, QVBoxLayout, QWidget, QStyleFactory, QMainWindow, QLabel, QListWidget,
                               QCheckBox)


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
        self.left_layout.addWidget(self.image_label)

        self.ingrediens_label = QLabel("SELECT INGREDIENTS")
        self.ingrediens_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingrediens_label.setStyleSheet("font-weight: bold;")
        self.left_layout.addWidget(self.ingrediens_label)

        self.selected_ingrediens = []
        # Wyświetlanie elementów listy składników

        for ingredient in ingredients:
            # Tworzę QCheckBox
            self.checkbox = QCheckBox(ingredient)
            self.checkbox.setChecked(False)  # Domyślnie zaznaczony
            self.left_layout.addWidget(self.checkbox)
            self.selected_ingrediens.append(ingredient)

        # Tworzę wertykalny right_layout
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout)

        # Przycisk "Generate Recipes" na samej górze
        self.button = QPushButton("Generate Recipes")
        self.button.clicked.connect(self.generate_recipes)
        self.right_layout.addWidget(self.button, alignment=Qt.AlignTop)

        self.recipes_list = QListWidget()
        self.right_layout.addWidget(self.recipes_list)

    def generate_recipes(self):
        # todo algorytm wyszukujacy przepisy - do napisania

        # selected_ingredients = [
        #     self.ingredients_list.item(i).text()
        #     for i in range(self.ingredients_list.count())
        # ]
        # print("Selected Ingredients:", selected_ingredients)
        #
        # # Wyświetlanie przepisów po kliknięciu przycisku
        # self.recipes_list.clear()
        # matching_recipes = [recipe for recipe in self.recipes if
        #                     all(ingredient in selected_ingredients for ingredient in recipe["ingredients"])]
        # if matching_recipes:
        #     for recipe in matching_recipes:
        #         self.recipes_list.addItem(recipe["name"])
        # else:
        #     self.recipes_list.addItem("No recipes found")
        self.recipes_list.addItems(self.recipes)


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
    ingredients = ['Milk', 'Eggs', 'Flour', 'Chicken']
    recipes = ['Scrambled Eggs', 'Pancakes', 'Chicken Soup', 'Baked Chicken']

    dialog = QDialog()
    ui = MainWindow(ingredients, recipes)
    ui.show()
    sys.exit(app.exec())
