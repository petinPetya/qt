from PIL import Image, ImageEnhance
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from canvas.canvas import *
from qssstyles.styles import *


class PaintApp(QMainWindow):
    builtins_caps = {
        "kp1": Qt.PenCapStyle.RoundCap,
        "kp2": Qt.PenCapStyle.FlatCap,
        "kp3": Qt.PenCapStyle.SquareCap,
    }

    builtins_filters = {
        "st1": ImageEnhance.Contrast,
        "st2": ImageEnhance.Brightness,
        "st3": ImageEnhance.Sharpness,
        "st4": ImageEnhance.Color,
    }

    names = ["roundcap", "flatcap", "squarecap"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Govno")
        self.setGeometry(100, 100, 800, 600)

        # Главный виджет и компоновка
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title
        self.title = QLabel("ЫЫЫЫЫЫ!!")
        self.title.setStyleSheet(text_style_title)
        self.title.setFixedSize(QSize(800, 40))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title)

        # Создаем QTabWidget для инструментов
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        main_layout.addWidget(self.tab_widget)

        # Создаем холст
        self.canvas = Canvas()

        main_layout.addWidget(self.canvas, 1)
        # Создаем вкладки
        self.create_file_tab()
        self.create_tools_tab()
        self.create_edit_widget()

    def create_file_tab(self):
        file_tab = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        # Кнопка открытия файла
        open_btn = QPushButton("Открыть")
        open_btn.clicked.connect(self.open_file)
        layout.addWidget(open_btn)

        # Кнопка выхода
        exit_btn = QPushButton("Выход")
        exit_btn.clicked.connect(QApplication.instance().quit)
        layout.addWidget(exit_btn)

        layout.addStretch()
        file_tab.setLayout(layout)
        self.tab_widget.addTab(file_tab, "Файл")

    def create_tools_tab(self):
        tools_tab = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        toolbar = QToolBar()
        # Кнопка очистки холста
        clear_action = QAction(QIcon.fromTheme("edit-clear"), "Очистить", self)
        clear_action.triggered.connect(self.canvas.clear)
        toolbar.addAction(clear_action)

        color_action = QAction(QIcon.fromTheme("color-picker"), "Цвет", self)
        color_action.triggered.connect(self.choose_color)
        toolbar.addAction(color_action)
        self.colorlabel = QLabel(self)
        self.colorlabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.colorlabel.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.colorlabel.setFixedSize(48, 20)
        toolbar.addWidget(self.colorlabel)

        # Слайдер для толщины кисти
        toolbar.addWidget(QLabel("Толщина:"))
        widt = QSpinBox()
        widt.setFixedSize(90, 20)
        widt.setRange(0, 1000)
        widt.setValue(self.canvas.pen_width)
        widt.valueChanged.connect(self.set_pen_width)
        toolbar.addWidget(widt)
        toolbar.layout().setSpacing(8)

        change_cap_buttons = QHBoxLayout()
        setattr(self, "st1", QPushButton())
        setattr(self, "st2", QPushButton())
        setattr(self, "st3", QPushButton())
        buttons1 = [self.st1, self.st2, self.st3]
        cnt = 0
        for i in buttons1:
            cnt += 1
            i.setIcon(QIcon(f"static/{PaintApp.names[cnt - 1]}.jpg"))
            i.setObjectName(f"kp{cnt}")
            i.clicked.connect(self.change_cap)
            i.setStyleSheet(button_cap_style)
            change_cap_buttons.addWidget(i)
        change_cap_buttons.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(toolbar)
        layout.addLayout(change_cap_buttons)
        tools_tab.setLayout(layout)
        self.tab_widget.addTab(tools_tab, "Инструменты")

    def create_edit_widget(self):
        edit_tab = QWidget()

        main_layout = QHBoxLayout(edit_tab)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(8, 8, 8, 8)

        filters_container = QWidget()
        filters_container.setStyleSheet(container_style)
        filters_layout = QGridLayout(filters_container)
        filters_layout.setSpacing(5)
        filters_layout.setContentsMargins(8, 8, 8, 8)
        filter_data = ["Контраст", "Яркость", "Резкость", "Цвета"]

        for row, btn_name in enumerate(filter_data):
            setattr(self, btn_name, QPushButton(btn_name))
            btn = getattr(self, btn_name)
            btn.setObjectName("st" + str(row + 1))
            btn.setFixedSize(70, 20)
            btn.setStyleSheet(filter_button_style)
            btn.clicked.connect(self.open_dialog)
            filters_layout.addWidget(btn, row, 0)

        rgb_container = QWidget()
        rgb_container.setStyleSheet(container_style)
        rgb_layout = QVBoxLayout(rgb_container)
        rgb_layout.setSpacing(5)
        rgb_layout.setContentsMargins(8, 8, 8, 8)

        rgb_title = QLabel("RGB Каналы")
        rgb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rgb_title.setStyleSheet(
            "font-size: 9px; font-weight: bold;"
            "color: #495057; margin-bottom: 5px;",
        )
        rgb_layout.addWidget(rgb_title)

        rgb_data = [
            ("R", "rgb_red", "#dc3545"),
            ("G", "rgb_green", "#28a745"),
            ("B", "rgb_blue", "#007bff"),
        ]

        for text, btn_name, color in rgb_data:
            setattr(self, btn_name, QPushButton(text))
            btn = getattr(self, btn_name)
            btn.setFixedSize(50, 20)
            btn.setStyleSheet(filter_button_style)
            btn.clicked.connect(self.open_dialog)
            rgb_layout.addWidget(btn)

        main_layout.addWidget(filters_container)
        main_layout.addWidget(rgb_container)
        main_layout.addStretch()

        self.tab_widget.addTab(edit_tab, "Фильтры")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть изображение",
            "",
            "Images (*.png *.jpg *.bmp)",
        )
        if file_path:
            self.canvas.load_image(file_path)

    def qgraphicsview_to_pil(self, scene) -> Image:
        if scene is None:
            return None

        rect = scene.sceneRect()
        image = QImage(rect.size().toSize(), QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        scene.render(painter)
        painter.end()
        # Конвертируем QImage в PIL
        image = image.convertToFormat(QImage.Format.Format_RGBA8888)
        ptr = image.bits()
        ptr.setsize(image.sizeInBytes())

        pil_image = Image.frombytes(
            "RGBA",
            (image.width(), image.height()),
            ptr.asarray(),
            "raw",
            "RGBA",
            0,
            1,
        )
        return pil_image

    @staticmethod
    def pil_to_qimage(pil_image):
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        data = pil_image.tobytes("raw", "RGB")
        qimage = QImage(
            data,
            pil_image.width,
            pil_image.height,
            QImage.Format.Format_RGB888,
        )
        return qimage

    def add_pil_to_scene(self, imgp):
        imgq = imgp.toqimage()
        pixmap = QPixmap.fromImage(imgq)
        item = QGraphicsPixmapItem(pixmap)
        item.setPos(0, 0)

        self.canvas.scene.clear()
        self.canvas.scene.addItem(item)

    def choose_color(self):
        color = QColorDialog.getColor(
            self.canvas.pen_color,
            self,
            "Выберите цвет",
        )
        if color.isValid():
            self.canvas.pen_color = color
            self.colorlabel.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid black;",
            )

    def set_pen_width(self, width):
        self.canvas.pen_width = width

    # def set_image_contrast(self, value):
    #     self.editing = True
    #     self.img = self.qgraphicsview_to_pil(self.canvas.scene)
    #     if self.img:
    #         self.contrast = ImageEnhance.Contrast(self.img)
    #         self.img1 = self.contrast.enhance(value / 500.0)

    # def contrast_changed(self, e):
    #     if self.editing:
    #         self.add_pil_to_scene(self.img1)
    #         self.editing = False

    def change_cap(self, e):
        key = self.sender().objectName()
        print(key)
        if hasattr(self.canvas, "pen_cap"):
            setattr(
                self.canvas,
                "pen_cap",
                PaintApp.builtins_caps[key],
            )

    def open_dialog(self):
        sender_button = self.sender()
        filter_key = sender_button.objectName()

        # Сохраняем оригинальное изображение до любых изменений
        self.original_before_dialog = self.qgraphicsview_to_pil(
            self.canvas.scene,
        )

        dialog = uic.loadUi("ui/inhance_dialog.ui")
        dialog.setWindowTitle("Изменение фильтра")

        original_img = self.original_before_dialog
        if original_img:
            dialog.original_img = original_img
            dialog.filter_key = filter_key

            qimage = self.pil_to_qimage(original_img)
            pixmap = QPixmap.fromImage(qimage)
            dialog.label.setPixmap(pixmap)
            dialog.label.setScaledContents(True)

        def on_slider_changed(value):
            if hasattr(dialog, "original_img") and hasattr(
                dialog, "filter_key",
            ):
                image_before = PaintApp.builtins_filters[dialog.filter_key](
                    dialog.original_img,
                )
                normalized_value = (value + 50) / 50.0
                image_after = image_before.enhance(normalized_value)

                qimage_preview = self.pil_to_qimage(image_after)
                pixmap_preview = QPixmap.fromImage(qimage_preview)
                dialog.label.setPixmap(pixmap_preview)

        dialog.horizontalSlider.valueChanged.connect(on_slider_changed)

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            final_value = dialog.horizontalSlider.value()
            self.change_filter(final_value, filter_key)
        else:
            if hasattr(self, "original_before_dialog"):
                self.add_pil_to_scene(self.original_before_dialog)
                print("Изменения отменены")

    def change_filter(self, value, filter_key):
        # Используем сохраненный оригинал для чистого применения
        if hasattr(self, "original_before_dialog"):
            current_img = self.original_before_dialog
        else:
            current_img = self.qgraphicsview_to_pil(self.canvas.scene)

        if current_img:
            image_before = PaintApp.builtins_filters[filter_key](current_img)
            normalized_value = (value + 50) / 50.0  # Костыыыыыль!
            image_after = image_before.enhance(normalized_value)
            self.add_pil_to_scene(image_after)
            print(f"Фильтр {filter_key} применен со значением: {value}")
