from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from canvas.scene import CustomGraphicsView, FixedGraphicsScene


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 404)

        # Настройки кисти
        self.pen_color = QColor("#000000")
        self.pen_width = 5
        self.pen_style = Qt.PenStyle.SolidLine
        self.pen_cap = Qt.PenCapStyle.RoundCap

        # Фильтры
        self.contrast = 1
        self.brightness = 1
        self.sharpness = 1
        self.color = 1

        # Холст
        self.scene = FixedGraphicsScene(0, 0, 840, 567, self)
        self.scene.setSceneRect(0, 0, 840, 567)
        self.view = CustomGraphicsView(
            self.scene,
            self,
        )  # Используем кастомный view
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setInteractive(False)

        self.drawing = False
        self.last_point = QPointF()

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            return True
        return False

    def clear(self):
        self.scene.clear()

    def handle_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = self.view.mapToScene(event.pos())

    def handle_mouse_move(self, event):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            current_point = self.view.mapToScene(event.pos())
            line = QGraphicsLineItem(QLineF(self.last_point, current_point))
            line.setPen(
                QPen(
                    self.pen_color,
                    self.pen_width,
                    self.pen_style,
                    self.pen_cap,
                ),
            )
            self.scene.addItem(line)
            self.last_point = current_point

    def handle_mouse_release(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def get_visible_size(self):
        visible_rect = self.view.mapToScene(
            self.view.viewport().rect(),
        ).boundingRect()
        return visible_rect.size()

    def get_view_size(self):
        return self.view.size()
