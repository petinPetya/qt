from PIL import Image, ImageEnhance
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from canvas.canvas import *
from qssstyles.styles import *


class PaintApp(QMainWindow):
    builtins_caps = {
        "кп1": Qt.PenCapStyle.RoundCap,
        "кп2": Qt.PenCapStyle.FlatCap,
        "кп3": Qt.PenCapStyle.SquareCap,
    }

    builtins_filters = {
        "st1": ImageEnhance.Contrast,
        "st2": ImageEnhance.Brightness,
        "st3": ImageEnhance.Sharpness,
        "st4": ImageEnhance.Color,
    }

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
        setattr(self, "st1", QPushButton("кп1"))
        setattr(self, "st2", QPushButton("кп2"))
        setattr(self, "st3", QPushButton("кп3"))
        buttons1 = [self.st1, self.st2, self.st3]
        for i in buttons1:
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
        filters = QHBoxLayout()

        change_color_buttons = QVBoxLayout()
        setattr(self, "bt1", QPushButton("st1"))
        setattr(self, "bt2", QPushButton("st2"))
        setattr(self, "bt3", QPushButton("st3"))
        setattr(self, "bt4", QPushButton("st4"))
        buttons2 = [self.bt1, self.bt2, self.bt3, self.bt4]
        # self.cont = QSlider(Qt.Orientation.Horizontal, self)
        # self.cont.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # self.cont.setRange(0, 1000)
        # self.cont.setValue(500)
        # self.cont.sliderMoved.connect(self.contrast_changed)
        # self.cont.valueChanged.connect(self.set_image_contrast)
        for i in buttons2:
            # i.setSize(QSize(70, 30))
            i.clicked.connect(self.change_filter)
            change_color_buttons.addWidget(i)
        filters.addLayout(change_color_buttons)
        edit_tab.setLayout(filters)
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
        scene = self.canvas.scene
        if scene is None:
            return None
        rect = scene.sceneRect()
        image = QImage(rect.size().toSize(), QImage.Format.Format_ARGB32)
        image.fill(0)
        painter = QPainter(image)
        scene.render(painter, QRectF(image.rect()), rect)
        painter.end()
        pixmap = QPixmap.fromImage(image)

        qimage = pixmap.toImage()
        buffer = qimage.bits()
        buffer.setsize(qimage.bytesPerLine() * qimage.height())

        pil_image = Image.frombuffer(
            "RGBA",
            (qimage.width(), qimage.height()),
            bytes(buffer),
            "raw",
            "RGBA",
            0,
            1,
        )
        return pil_image

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
        key = self.sender().text()
        if hasattr(self.canvas, "pen_cap"):
            setattr(
                self.canvas,
                "pen_cap",
                PaintApp.builtins_caps[key],
            )

    def change_filter(self, value):
        key = self.sender().text()
        self.img = self.qgraphicsview_to_pil(self.canvas.scene)
        if self.img:
            image_before = PaintApp.builtins_filters[key](self.img)
            print(value)
            image_after = image_before.enhance(value / 500.0)
            self.add_pil_to_scene(image_after)
