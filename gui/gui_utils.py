from PySide6.QtCore import Qt
from PySide6.QtGui import QBitmap, QPainter, QPalette, QColor
from PySide6.QtWidgets import QStyleFactory


def create_round_mask(size):
    mask = QBitmap(size, size)
    mask.fill(Qt.color0)

    painter = QPainter(mask)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(Qt.color1)
    painter.setBrush(Qt.color1)
    painter.drawEllipse(0, 0, size, size)
    painter.end()

    return mask


def blue_theme(app):
    blue_palette = QPalette()
    blue_palette.setColor(QPalette.ColorRole.Window, QColor(204, 229, 255))
    blue_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 51, 102))
    blue_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    blue_palette.setColor(QPalette.ColorRole.Text, QColor(5, 2, 94))
    blue_palette.setColor(QPalette.ColorRole.Button, QColor(10, 100, 235))
    blue_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 51, 102))
    blue_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    blue_palette.setColor(QPalette.ColorRole.Link, QColor(0, 102, 204))
    blue_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 102, 204))
    blue_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 51, 102))

    updating_app_palette(app, blue_palette)


def violet_theme(app):
    violet_palette = QPalette()
    violet_palette.setColor(QPalette.ColorRole.Window, QColor(208, 181, 221))
    violet_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    violet_palette.setColor(QPalette.ColorRole.Text, QColor(69, 2, 94))
    violet_palette.setColor(QPalette.ColorRole.WindowText, QColor(70, 35, 105))
    violet_palette.setColor(QPalette.ColorRole.Button, QColor(115, 64, 152))
    violet_palette.setColor(QPalette.ColorRole.ButtonText, QColor(65, 30, 100))
    violet_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    violet_palette.setColor(QPalette.ColorRole.Link, QColor(174, 129, 255))
    violet_palette.setColor(QPalette.ColorRole.Highlight, QColor(174, 129, 255))
    violet_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(70, 35, 105))

    updating_app_palette(app, violet_palette)


def orange_theme(app):
    orange_palette = QPalette()
    orange_palette.setColor(QPalette.ColorRole.Window, QColor(255, 204, 153))
    orange_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    orange_palette.setColor(QPalette.ColorRole.Text, QColor(236, 69, 0))
    orange_palette.setColor(QPalette.ColorRole.WindowText, QColor(153, 76, 0))
    orange_palette.setColor(QPalette.ColorRole.Button, QColor(245, 125, 60))
    orange_palette.setColor(QPalette.ColorRole.ButtonText, QColor(130, 56, 0))
    orange_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    orange_palette.setColor(QPalette.ColorRole.Link, QColor(255, 128, 0))
    orange_palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 128, 0))
    orange_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(153, 76, 0))

    updating_app_palette(app, orange_palette)


def pink_theme(app):
    app.setStyle(QStyleFactory.create("Fusion"))
    pink_palette = QPalette()
    pink_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    pink_palette.setColor(QPalette.ColorRole.Window, QColor(255, 228, 225))
    pink_palette.setColor(QPalette.ColorRole.Text, QColor(128, 0, 0))
    pink_palette.setColor(QPalette.ColorRole.Button, QColor(255, 105, 180))
    pink_palette.setColor(QPalette.ColorRole.ButtonText, QColor(128, 0, 0))
    pink_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    pink_palette.setColor(QPalette.ColorRole.Link, QColor(255, 20, 147))
    pink_palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 20, 147))
    pink_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(128, 0, 0))

    app.setPalette(pink_palette)


def updating_app_palette(app, palette):
    app.setPalette(palette)
    for widget in app.allWidgets():
        widget.setPalette(palette)
