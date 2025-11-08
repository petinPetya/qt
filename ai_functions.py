import tempfile

from PyQt6.QtCore import pyqtSignal, QThread
import pytesseract


class OCRThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, image, language):
        super().__init__()
        self.image = image
        self.language = language

    def run(self):
        try:
            pytesseract.pytesseract.tesseract_cmd = r"C:\ptsr\tesseract.exe"

            # Сохраняется временно в файл для tesseract
            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False,
            ) as temp_file:
                self.image.save(temp_file.name)
                text = pytesseract.image_to_string(
                    temp_file.name,
                    lang=self.language,
                )
            self.finished.emit(text)
        except Exception as e:
            self.error.emit(str(e))
