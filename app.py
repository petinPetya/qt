from PIL import Image, ImageEnhance
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import pytesseract

from ai_functions import OCRThread
from canvas.canvas import *
from models.models import Login, Register
from qssstyles.styles import *

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\ptsr\\tesseract-ocr" r"-w64-setup-5.5.0.20241111.exe"
)


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
        self.setGeometry(100, 100, 1000, 600)

        # Текущий пользователь
        self.current_user = None

        # Главный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_widget = QWidget()
        left_widget.setMaximumWidth(300)  # Ограничиваем ширину
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        # Title
        self.title = QLabel("ЫЫЫЫЫЫ!!")
        self.title.setStyleSheet(text_style_title)
        self.title.setFixedHeight(40)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.title)

        # Создаем QTabWidget для инструментов
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        left_layout.addWidget(self.tab_widget)

        # Добавляем левый виджет в основную компоновку
        main_layout.addWidget(left_widget)

        # Создаем холст справа
        self.canvas = Canvas()
        main_layout.addWidget(self.canvas, 1)  # 1 - коэффициент растяжения

        # Создаем вкладки
        self.create_file_tab()
        self.create_tools_tab()
        self.create_edit_widget()
        self.create_ocr_tab()

    def start(self):
        """Метод для открытия формы аутентификации"""
        self.show_auth_dialog()

    def show_auth_dialog(self):
        """Показывает диалог аутентификации (регистрация/логин)"""
        login_dialog = Login(self)
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_user = login_dialog.get_current_user()
            print(f"Пользователь вошел: {self.current_user}")
            QMessageBox.information(
                self,
                "Успех",
                f"Добро пожаловать, {self.current_user.name}!",
            )
            self.update_user_info()
            return True
        return False

    def show_register_dialog(self):
        register_dialog = Register(self)
        if register_dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Успех", "Регистрация завершена!")
            return self.show_auth_dialog()
        return False

    def update_user_info(self):
        if self.current_user:
            self.user_info_label.setText(
                f"Пользователь: {self.current_user.name}",
            )
            self.user_info_label.setStyleSheet(
                "color: green; font-size: 10px;",
            )
        else:
            self.user_info_label.setText("Не авторизован")
            self.user_info_label.setStyleSheet("color: gray; font-size: 10px;")

    def create_file_tab(self):
        file_tab = QWidget()
        layout = QVBoxLayout()  # Изменил на вертикальную
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Кнопка открытия файла
        open_btn = QPushButton("Открыть")
        open_btn.clicked.connect(self.open_file)
        layout.addWidget(open_btn)

        # Кнопка входа/регистрации
        auth_btn = QPushButton("Вход / Регистрация")
        auth_btn.clicked.connect(self.start)
        layout.addWidget(auth_btn)

        # Информация о пользователе
        self.user_info_label = QLabel("Не авторизован")
        self.user_info_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.user_info_label)

        # Кнопка выхода
        exit_btn = QPushButton("Выход")
        exit_btn.clicked.connect(QApplication.instance().quit)
        layout.addWidget(exit_btn)

        layout.addStretch()
        file_tab.setLayout(layout)
        self.tab_widget.addTab(file_tab, "Файл")

    # ОСТАЛЬНЫЕ МЕТОДЫ ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ

    def create_tools_tab(self):
        tools_tab = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Вертикальный тулбар
        toolbar = QToolBar()
        toolbar.setOrientation(Qt.Orientation.Vertical)  # Вертикальный тулбар

        # Кнопка очистки холста
        clear_action = QAction(QIcon.fromTheme("edit-clear"), "Очистить", self)
        clear_action.triggered.connect(self.canvas.clear)
        toolbar.addAction(clear_action)

        color_action = QAction(QIcon.fromTheme("color-picker"), "Цвет", self)
        color_action.triggered.connect(self.choose_color)
        toolbar.addAction(color_action)

        self.colorlabel = QLabel(self)
        self.colorlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.colorlabel.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.colorlabel.setFixedSize(60, 25)
        toolbar.addWidget(self.colorlabel)

        # Слайдер для толщины кисти
        thickness_widget = QWidget()
        thickness_layout = QHBoxLayout(thickness_widget)
        thickness_layout.setContentsMargins(0, 0, 0, 0)
        thickness_layout.addWidget(QLabel("Толщина:"))
        widt = QSpinBox()
        widt.setFixedSize(70, 25)
        widt.setRange(0, 1000)
        widt.setValue(self.canvas.pen_width)
        widt.valueChanged.connect(self.set_pen_width)
        thickness_layout.addWidget(widt)
        toolbar.addWidget(thickness_widget)

        layout.addWidget(toolbar)

        # Кнопки стилей пера
        change_cap_buttons = QVBoxLayout()  # Вертикальное расположение
        change_cap_buttons.setSpacing(5)

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
            i.setFixedHeight(40)
            change_cap_buttons.addWidget(i)

        layout.addLayout(change_cap_buttons)
        layout.addStretch()
        tools_tab.setLayout(layout)
        self.tab_widget.addTab(tools_tab, "Инструменты")

    def create_edit_widget(self):
        edit_tab = QWidget()

        main_layout = QVBoxLayout(edit_tab)  # Вертикальная компоновка
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(8, 8, 8, 8)

        filters_container = QWidget()
        filters_container.setStyleSheet(container_style)
        filters_layout = QVBoxLayout(filters_container)  # Вертикальная
        filters_layout.setSpacing(5)
        filters_layout.setContentsMargins(8, 8, 8, 8)
        filter_data = ["Контраст", "Яркость", "Резкость", "Цвета"]

        for btn_name in filter_data:
            setattr(self, btn_name, QPushButton(btn_name))
            btn = getattr(self, btn_name)
            btn.setObjectName("st" + str(filter_data.index(btn_name) + 1))
            btn.setFixedHeight(30)
            btn.setStyleSheet(filter_button_style)
            btn.clicked.connect(self.open_enh_dialog)
            filters_layout.addWidget(btn)

        rgb_container = QWidget()
        rgb_container.setStyleSheet(container_style)
        rgb_layout = QVBoxLayout(rgb_container)
        rgb_layout.setSpacing(5)
        rgb_layout.setContentsMargins(8, 8, 8, 8)

        rgb_data = [
            ("R", "rgb_red", "#dc3545"),
            ("G", "rgb_green", "#28a745"),
            ("B", "rgb_blue", "#007bff"),
            ("A", "rgb_alpha", "#c7b1cd"),
        ]

        for text, btn_name, color in rgb_data:
            setattr(self, btn_name, QPushButton(text))
            btn = getattr(self, btn_name)
            btn.setFixedHeight(30)
            btn.setStyleSheet(filter_button_style)
            btn.clicked.connect(self.open_col_dialog)
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

    def create_ocr_tab(self):
        """Создаем упрощенную вкладку OCR"""
        ocr_tab = QWidget()
        layout = QVBoxLayout(ocr_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Выбор языка
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Язык:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(
            ["eng", "rus", "fra", "deu", "spa", "chi_sim", "jpn"],
        )
        self.lang_combo.setCurrentText("eng")
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # Кнопка распознавания с текущего холста
        self.recognize_btn = QPushButton("Распознать текст с холста")
        self.recognize_btn.clicked.connect(self.recognize_from_canvas)
        layout.addWidget(self.recognize_btn)

        # Область для текста
        layout.addWidget(QLabel("Распознанный текст:"))
        self.ocr_text_browser = QTextBrowser()
        self.ocr_text_browser.setPlaceholderText(
            "Текст появится здесь после распознавания...",
        )
        layout.addWidget(self.ocr_text_browser)

        # Нижняя панель
        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(5)

        # Прогресс бар
        self.ocr_progress_bar = QProgressBar()
        self.ocr_progress_bar.setVisible(False)
        bottom_layout.addWidget(self.ocr_progress_bar)

        # Информационная метка
        self.ocr_info_label = QLabel("Готов к работе")
        bottom_layout.addWidget(self.ocr_info_label)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.ocr_save_btn = QPushButton("Сохранить текст")
        self.ocr_save_btn.clicked.connect(self.save_ocr_text)
        self.ocr_save_btn.setEnabled(False)
        buttons_layout.addWidget(self.ocr_save_btn)

        clear_btn = QPushButton("Очистить")
        clear_btn.clicked.connect(self.clear_ocr_text)
        buttons_layout.addWidget(clear_btn)

        bottom_layout.addLayout(buttons_layout)
        layout.addLayout(bottom_layout)

        # Переменные для OCR
        self.ocr_thread = None

        self.tab_widget.addTab(ocr_tab, "OCR")

    def recognize_from_canvas(self):
        """Распознает текст с текущего холста"""
        scene_image = self.qgraphicsview_to_pil(self.canvas.scene)
        if not scene_image:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "На холсте нет изображения!",
            )
            return

        self.ocr_progress_bar.setVisible(True)
        self.ocr_progress_bar.setRange(0, 0)  # Индикатор прогресса
        self.recognize_btn.setEnabled(False)
        self.ocr_info_label.setText("Распознавание текста...")

        # Запускаем в отдельном потоке
        language = self.lang_combo.currentText()
        self.ocr_thread = OCRThread(scene_image, language)
        self.ocr_thread.finished.connect(self.on_ocr_finished)
        self.ocr_thread.error.connect(self.on_ocr_error)
        self.ocr_thread.start()

    def on_ocr_finished(self, text):
        """Обрабатывает завершение распознавания"""
        self.ocr_progress_bar.setVisible(False)
        self.recognize_btn.setEnabled(True)
        self.ocr_text_browser.setPlainText(text)
        self.ocr_save_btn.setEnabled(bool(text.strip()))

        # Статистика
        char_count = len(text)
        word_count = len(text.split())
        line_count = len(text.split("\n"))

        self.ocr_info_label.setText(
            (
                f"Готово. Символов: {char_count},"
                f"Слов: {word_count}, Строк: {line_count}"
            ),
        )

    def on_ocr_error(self, error_message):
        """Обрабатывает ошибки распознавания"""
        self.ocr_progress_bar.setVisible(False)
        self.recognize_btn.setEnabled(True)
        QMessageBox.critical(
            self,
            "Ошибка",
            f"Ошибка распознавания:\n{error_message}",
        )
        self.ocr_info_label.setText("Ошибка распознавания")

    def save_ocr_text(self):
        """Сохраняет распознанный текст в файл"""
        text = self.ocr_text_browser.toPlainText()
        if not text.strip():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить текст",
            "",
            "Text Files (*.txt);;All Files (*)",
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                self.ocr_info_label.setText(f"Текст сохранен в: {file_path}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Не удалось сохранить файл:\n{e}",
                )

    def clear_ocr_text(self):
        """Очищает область с текстом"""
        self.ocr_text_browser.clear()
        self.ocr_save_btn.setEnabled(False)
        self.ocr_info_label.setText("Текст очищен")

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

    def change_cap(self, e):
        key = self.sender().objectName()
        print(key)
        if hasattr(self.canvas, "pen_cap"):
            setattr(
                self.canvas,
                "pen_cap",
                PaintApp.builtins_caps[key],
            )

    def open_enh_dialog(self):
        sender_button = self.sender()
        filter_key = sender_button.objectName()

        # Сохраняем оригинальное изображение до любых изменений
        self.original_before_dialog = self.qgraphicsview_to_pil(
            self.canvas.scene,
        )

        dialog = uic.loadUi("ui/inhance_dialog.ui")
        chan_type = ["фильтра", "цветового канала"][
            sender_button.text() in "RGBA"
        ]
        dialog.setWindowTitle("Изменение " + chan_type)

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
                dialog,
                "filter_key",
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

    def open_col_dialog(self):
        """Открывает диалоговое окно для настройки цветовых каналов"""
        # Сохраняем оригинальное изображение
        self.original_before_dialog = self.qgraphicsview_to_pil(
            self.canvas.scene,
        )

        if not self.original_before_dialog:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Нет изображения для редактирования!",
            )
            return

        # Создаем диалоговое окно
        dialog = QDialog(self)
        dialog.setWindowTitle("Настройка цветовых каналов")
        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout(dialog)

        # Метка для изображения
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumSize(480, 240)
        image_label.setStyleSheet(
            "border: 1px solid #ccc; background-color: #f8f9fa;",
        )
        layout.addWidget(image_label)

        # Область для ползунков
        sliders_layout = QVBoxLayout()

        # Ползунок для красного канала
        red_layout = QHBoxLayout()
        red_label = QLabel("Красный (R):")
        red_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        red_slider = QSlider(Qt.Orientation.Horizontal)
        red_slider.setRange(-100, 100)
        red_slider.setValue(0)
        red_value = QLabel("0")
        red_value.setFixedWidth(30)
        red_layout.addWidget(red_label)
        red_layout.addWidget(red_slider)
        red_layout.addWidget(red_value)
        sliders_layout.addLayout(red_layout)

        # Ползунок для зеленого канала
        green_layout = QHBoxLayout()
        green_label = QLabel("Зеленый (G):")
        green_label.setStyleSheet("color: #28a745; font-weight: bold;")
        green_slider = QSlider(Qt.Orientation.Horizontal)
        green_slider.setRange(-100, 100)
        green_slider.setValue(0)
        green_value = QLabel("0")
        green_value.setFixedWidth(30)
        green_layout.addWidget(green_label)
        green_layout.addWidget(green_slider)
        green_layout.addWidget(green_value)
        sliders_layout.addLayout(green_layout)

        # Ползунок для синего канала
        blue_layout = QHBoxLayout()
        blue_label = QLabel("Синий (B):")
        blue_label.setStyleSheet("color: #007bff; font-weight: bold;")
        blue_slider = QSlider(Qt.Orientation.Horizontal)
        blue_slider.setRange(-100, 100)
        blue_slider.setValue(0)
        blue_value = QLabel("0")
        blue_value.setFixedWidth(30)
        blue_layout.addWidget(blue_label)
        blue_layout.addWidget(blue_slider)
        blue_layout.addWidget(blue_value)
        sliders_layout.addLayout(blue_layout)

        layout.addLayout(sliders_layout)

        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # Функция для обновления предпросмотра
        def update_preview():
            red_val = red_slider.value()
            green_val = green_slider.value()
            blue_val = blue_slider.value()

            # Обновляем значения
            red_value.setText(str(red_val))
            green_value.setText(str(green_val))
            blue_value.setText(str(blue_val))

            # Применяем изменения к изображению
            modified_img = self.apply_color_channels(
                self.original_before_dialog,
                red_val,
                green_val,
                blue_val,
            )

            # Обновляем предпросмотр
            qimage = self.pil_to_qimage(modified_img)
            pixmap = QPixmap.fromImage(qimage)
            scaled_pixmap = pixmap.scaled(
                480,
                240,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            image_label.setPixmap(scaled_pixmap)

        # Подключаем сигналы
        red_slider.valueChanged.connect(update_preview)
        green_slider.valueChanged.connect(update_preview)
        blue_slider.valueChanged.connect(update_preview)

        # Первоначальный предпросмотр
        update_preview()

        # Показываем диалог
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Применяем финальные изменения
            red_val = red_slider.value()
            green_val = green_slider.value()
            blue_val = blue_slider.value()

            final_img = self.apply_color_channels(
                self.original_before_dialog,
                red_val,
                green_val,
                blue_val,
            )
            self.add_pil_to_scene(final_img)
            print(
                f"Каналы: R={red_val}, G={green_val}, B={blue_val}",
            )
        else:
            # Восстанавливаем оригинал
            if hasattr(self, "original_before_dialog"):
                self.add_pil_to_scene(self.original_before_dialog)
                print("Изменения цветовых каналов отменены")

    def apply_color_channels(self, image, red_value, green_value, blue_value):
        """Применяет изменения к цветовым каналам через PIL"""
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Разделяем каналы
        r, g, b = image.split()

        # Применяем изменения к каждому каналу
        def adjust_channel(channel, value):
            if value > 0:
                # Увеличиваем яркость канала
                enhancer = ImageEnhance.Brightness(channel)
                return enhancer.enhance(1 + value / 100.0)
            elif value < 0:
                # Уменьшаем яркость канала
                enhancer = ImageEnhance.Brightness(channel)
                return enhancer.enhance(1 + value / 100.0)
            else:
                return channel

        r_modified = adjust_channel(r, red_value)
        g_modified = adjust_channel(g, green_value)
        b_modified = adjust_channel(b, blue_value)

        # Объединяем каналы обратно
        return Image.merge("RGB", (r_modified, g_modified, b_modified))
