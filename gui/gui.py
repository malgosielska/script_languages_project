import sys

from PySide6.QtCore import (Qt, QSize)
from PySide6.QtGui import (QPalette, QPixmap, QIcon)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout,
                               QPushButton, QVBoxLayout, QWidget, QMainWindow, QLabel, QListWidget,
                               QCheckBox, QScrollArea, QLineEdit, QGridLayout)

from database_handler.ingredient_autocompleting import search_ingredients_by_prefix
from database_handler.recipe_generator import get_recipes_by_ingredients, get_details_by_name
from database_handler.utils import get_ingredients_names, get_recipes_names
from gui_utils import create_round_mask, blue_theme, orange_theme, violet_theme, pink_theme


class MainWindow(QMainWindow):

    def __init__(self, ingredients, recipes, avatar):
        super().__init__()
        self.avatar = avatar
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
        self.image_label.setPixmap(QPixmap(self.avatar).scaledToWidth(100))
        self.image_label.setFixedSize(100, 100)
        self.image_label.setMask(create_round_mask(100))
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
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
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


class AvatarSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("avatar")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.window_icon = QIcon("cooking_icon.jpg")
        self.setWindowIcon(self.window_icon)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.avatar_label = QLabel("Choose your avatar and theme")

        self.avatar_label.setStyleSheet("color: black;font-weight: bold;font-size: 30px;")
        self.avatar_label.setFixedHeight(50)

        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.avatar_label)

        self.central_layout = QGridLayout()

        self.main_layout.addLayout(self.central_layout)

        # creating buttons with available avatars
        for i in range(1, 7):
            self.avatar_button = QPushButton()
            self.avatar_button.setFixedSize(150, 150)
            self.avatar_file = f"avatars/avatar_{i}.jpg"
            self.avatar_button.setIcon(QIcon(self.avatar_file))
            self.avatar_button.setIconSize(QSize(150, 150))
            self.avatar_button.clicked.connect(self.open_main_window)
            self.avatar_button.setMask(create_round_mask(150))
            self.central_layout.addWidget(self.avatar_button, (i - 1) // 3, (i - 1) % 3)

            self.avatar_button.path = self.avatar_file

    def open_main_window(self):

        self.ui = MainWindow(ingredients, recipes, self.sender().path)
        self.ui.show()
        self.changing_theme()
        self.close()

    def changing_theme(self):
        theme = self.sender().path
        match theme:
            case "avatars/avatar_1.jpg":
                blue_theme(app)
            case "avatars/avatar_2.jpg":
                blue_theme(app)
            case "avatars/avatar_5.jpg":
                orange_theme(app)
            case "avatars/avatar_6.jpg":
                violet_theme(app)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    pink_theme(app)

    ingredients = get_ingredients_names()
    recipes = get_recipes_names()

    dialog = QDialog()
    ui = AvatarSelectionWindow()
    ui.show()
    sys.exit(app.exec())
