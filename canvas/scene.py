from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class FixedGraphicsScene(QGraphicsScene):
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)
        self.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        self.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)

    def mouseMoveEvent(self, event):
        event.ignore()

    def wheelEvent(self, event):
        event.ignore()


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, canvas):
        super().__init__(scene)
        self.canvas = canvas
        self.scene = scene
        self.fitInView(
            self.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )

        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.canvas.handle_mouse_press(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.canvas.handle_mouse_move(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.canvas.handle_mouse_release(event)
        super().mouseReleaseEvent(event)
