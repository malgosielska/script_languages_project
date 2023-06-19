import sys

from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QColor, QPalette, QPixmap, QIcon)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout,
                               QPushButton, QVBoxLayout, QWidget, QStyleFactory, QMainWindow, QLabel, QListWidget,
                               QCheckBox, QScrollArea, QLineEdit, QGridLayout)

from database_handler.ingredient_autocompleting import search_ingredients_by_prefix
from database_handler.recipe_generator import get_recipes_by_ingredients, get_details_by_name
from database_handler.utils import get_ingredients_names, get_recipes_names


class MainWindow(QMainWindow):

    def __init__(self, ingredients, recipes):
        super().__init__()

        self.ingredients = ingredients
        self.recipes = recipes

        self.setWindowTitle("Recipe Generator")
        self.setMinimumWidth(1000)
        self.window_icon = QIcon("cooking_icon.jpg")
        self.setWindowIcon(self.window_icon)
        # added central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # horizontal layout
        self.main_layout = QHBoxLayout(self.central_widget)

        # vertical layout
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

        # added picture in left corner
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap("pink_lady.jpg").scaledToWidth(100))
        self.image_label.setFixedSize(100, 100)
        self.left_layout.addWidget(self.image_label)

        self.ingrediens_label = QLabel("SELECT INGREDIENTS")
        self.ingrediens_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingrediens_label.setStyleSheet("color: black;font-weight: bold;font-size: 15px;")
        self.ingrediens_label.setFixedSize(400, 30)
        self.left_layout.addWidget(self.ingrediens_label)

        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("font-size: 14px;")
        self.left_layout.addWidget(self.search_input)
        self.left_layout.addWidget(self.search_button)

        self.selected_ingredients = []
        self.checkboxes_list = []

        # adding checkboxes with available ingredients
        self.checkboxes_widget = QWidget()
        self.checkboxes_layout = QVBoxLayout()

        self.checkboxes_widget.setLayout(self.checkboxes_layout)
        self.make_checkboxes(ingredients, False)

        self.search_button.clicked.connect(self.search_ingredients_by_prefix)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # adding scroll area
        self.scroll_area.setWidget(self.checkboxes_widget)
        self.left_layout.addWidget(self.scroll_area)
        # adding buttons at the bottom of left_layout
        # button that adds selected ingredients
        self.button_add_selected = QPushButton("Add selected")
        self.button_add_selected.setStyleSheet("font-size: 14px;")
        # button that selects all ingredients
        self.button_select_all = QPushButton("Select all")
        self.button_select_all.setStyleSheet("font-size: 14px;")
        # button that unselects all ingredients
        self.button_unselect_all = QPushButton("Unselect all")
        self.button_unselect_all.setStyleSheet("font-size: 14px;")

        self.left_layout.addWidget(self.button_add_selected)
        self.left_layout.addWidget(self.button_select_all)
        self.left_layout.addWidget(self.button_unselect_all)

        self.left_layout.addStretch(1)
        # connecting buttons to functions
        self.button_select_all.clicked.connect(self.select_all)
        self.button_unselect_all.clicked.connect(self.unselect_all)
        self.button_add_selected.clicked.connect(self.add_selected)

        # creating central layout that shows the list of selected ingredients by a user
        self.central_layout = QVBoxLayout()
        self.main_layout.addLayout(self.central_layout)

        self.selected_label = QLabel("SELECTED INGREDIENTS")
        self.selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_label.setStyleSheet("color: black;font-weight: bold;font-size: 15px")
        self.selected_label.setFixedSize(200, 30)
        self.central_layout.addWidget(self.selected_label)

        self.selected_i = QListWidget()
        list_palette = self.selected_i.palette()
        list_palette.setColor(QPalette.ColorRole.Base, Qt.white)
        self.selected_i.setPalette(list_palette)
        self.selected_i.setStyleSheet("font-size:14px")
        self.central_layout.addWidget(self.selected_i)

        # adding buttons that let delete selected ingredients
        self.button = QPushButton("Delete")
        self.button.setStyleSheet("font-size: 14px;")

        self.del_all = QPushButton("Delete all")
        self.del_all.setStyleSheet("font-size: 14px;")

        self.central_layout.addWidget(self.button, alignment=Qt.AlignBottom)
        self.button.clicked.connect(self.delete)
        self.central_layout.addWidget(self.del_all)
        self.del_all.clicked.connect(self.delete_all)

        # adding right layout
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout)

        # adding button that generates recipes based on selected ingredients
        self.button = QPushButton("Generate Recipes")
        self.button.setStyleSheet("font-size: 14px;")
        self.button.clicked.connect(self.generate_recipes)
        self.right_layout.addWidget(self.button, alignment=Qt.AlignTop)

        self.recipes_list = QListWidget()
        list_palette = self.recipes_list.palette()
        list_palette.setColor(QPalette.ColorRole.Base, Qt.white)
        self.recipes_list.setPalette(list_palette)
        self.right_layout.addWidget(self.recipes_list)
        # opening details to the selected recipe
        self.recipes_list.itemClicked.connect(self.opening_instructions)
        self.selected_i.itemClicked.connect(self.delete_selected_i)
        self.recipes_list.setStyleSheet("font-size: 14px;")

    def handle_checkbox(self):

        selected_ingredients = []
        for checkbox in self.checkboxes_list:
            ingredient = checkbox.text()

            if checkbox.isChecked():
                selected_ingredients.append(ingredient)
        return selected_ingredients

    def make_checkboxes(self, my_ingredients, checked):
        self.checkboxes_list.clear()
        for ingredient in my_ingredients:
            # Tworzę QCheckBox
            self.checkbox = QCheckBox(ingredient)
            self.checkbox.setStyleSheet("color: black; QCheckBox: white; font-size: 14px;")
            if checked:
                self.checkbox.setChecked(True)
            else:
                self.checkbox.setChecked(False)
            # self.checkbox.stateChanged.connect(self.handle_checkbox)
            self.checkboxes_list.append(self.checkbox)
            self.checkboxes_layout.setAlignment(Qt.AlignTop)
            self.checkboxes_layout.addWidget(self.checkbox)

    def search_ingredients_by_prefix(self):
        # creating a call to the database
        self.selected_ingredients = list(set(self.selected_ingredients + (self.handle_checkbox())))
        self.selected_i.clear()
        self.selected_i.addItems(self.selected_ingredients)
        layout = self.checkboxes_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        prefix = self.search_input.text()

        self.make_checkboxes(search_ingredients_by_prefix(prefix), False)

    def add_selected(self):
        self.selected_ingredients = list(set(self.selected_ingredients + (self.handle_checkbox())))
        self.selected_i.clear()
        self.selected_i.addItems(self.selected_ingredients)

    def select_all(self):
        layout = self.checkboxes_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.make_checkboxes(ingredients, True)

    def unselect_all(self):
        layout = self.checkboxes_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.make_checkboxes(ingredients, False)

    def generate_recipes(self):

        self.selected_i.clear()
        self.selected_i.addItems(self.selected_ingredients)
        self.recipes_list.clear()
        recipe = get_recipes_by_ingredients(self.selected_ingredients)
        if recipe:
            self.recipes_list.addItems(recipe)
        else:
            self.recipes_list.addItem("No recipes found")

    def delete_selected_i(self, item):
        self.selected_item = item.text()

    def delete(self):
        self.selected_ingredients.remove(self.selected_item)
        self.selected_i.clear()
        self.selected_i.addItems(self.selected_ingredients)

    def delete_all(self):
        self.selected_ingredients.clear()
        self.selected_i.clear()

    def opening_instructions(self, item):
        selected_item = item.text()
        next_window = NextWindow(selected_item)
        next_window.exec()


# next window which are details to a selected recipe
class NextWindow(QDialog):
    def __init__(self, item):
        super().__init__()

        self.item = item
        self.setWindowTitle("Recipe")
        self.setMinimumWidth(1300)
        self.setMinimumHeight(600)
        self.window_icon = QIcon("cooking_icon.jpg")
        self.setWindowIcon(self.window_icon)
        self.layout = QGridLayout()

        self.label = QLabel(self.item)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label.setStyleSheet("font-size: 40px;color: black;font-weight: bold;")
        self.label.setFixedHeight(100)

        # adding vertical layout
        self.ingredients_label = QLabel("Ingredients")
        self.ingredients_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ingredients_label.setFixedHeight(50)
        self.ingredients_label.setStyleSheet("font-size: 25px;color: black;font-weight: bold;")

        self.instructions_label = QLabel("Instructions")
        self.instructions_label.setStyleSheet("font-size: 25px;color: black;font-weight: bold;")
        self.instructions_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # list of ingredients needed in the recipe
        self.ingredients_text = QLabel(get_details_by_name(item)[0])
        self.ingredients_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ingredients_text.setStyleSheet("font-size: 20px;color: black;")

        # list of instructions for the recipe
        self.instructions_text = QLabel(get_details_by_name(item)[1])
        self.instructions_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.instructions_text.setStyleSheet("font-size: 20px;color: black;")

        self.layout.addWidget(self.label, 0, 0, 1, 2)
        self.layout.addWidget(self.ingredients_label, 1, 0)
        self.layout.addWidget(self.instructions_label, 1, 1)
        self.layout.addWidget(self.ingredients_text, 2, 0)
        self.layout.addWidget(self.instructions_text, 2, 1)

        self.setLayout(self.layout)


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

    ingredients = get_ingredients_names()
    recipes = get_recipes_names()

    dialog = QDialog()
    ui = MainWindow(ingredients, recipes)
    ui.show()
    sys.exit(app.exec())
