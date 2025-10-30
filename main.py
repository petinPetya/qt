#!/usr/bin/env python
import sys

from PyQt6.QtWidgets import QApplication
from app import PaintApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec())
