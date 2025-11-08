from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)
from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates

Base = declarative_base()
engine = create_engine("sqlite:///users.db", echo=True)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    name_normalized = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    description_length = Column(Integer, default=70)

    @validates("password")
    def checkPassword(self, key, password):
        if len(password) < 8:
            raise ValueError("Пароль слишком короткий! Минимум 8 символов")
        return password

    @validates("name")
    def checkName(self, key, name):
        if not name or not name[0].isalpha():
            raise ValueError("Имя должно начинаться с буквы!")
        self.name_normalized = name.lower()
        return name

    @validates("email")
    def checkEmail(self, key, email):
        if "@" not in email or "." not in email:
            raise ValueError("Некорректный email адрес!")
        return email

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"


Base.metadata.create_all(engine)


class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вход")
        self.setFixedSize(400, 300)
        self.current_user = None

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title_label = QLabel("Вход в систему")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        form_layout = QFormLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setMinimumSize(200, 30)
        self.username_edit.setPlaceholderText("Введите имя пользователя")
        form_layout.addRow("Имя пользователя:", self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumSize(200, 30)
        self.password_edit.setPlaceholderText("Введите пароль")
        form_layout.addRow("Пароль:", self.password_edit)

        layout.addLayout(form_layout)

        register_label = QLabel(
            '<a href="register">Нет аккаунта? Зарегистрироваться...</a>',
        )
        register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_label.linkActivated.connect(self.show_register)
        layout.addWidget(register_label)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
        )
        self.button_box.accepted.connect(self.validate_login)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def show_register(self):
        self.reject()
        register_dialog = Register(self.parent())
        register_dialog.exec()

    def validate_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()

        if not all([username, password]):
            QMessageBox.warning(
                self,
                "Ошибка",
                "Все поля должны быть заполнены!",
            )
            return

        session = Session()

        try:
            user = session.query(User).filter(User.name == username).first()

            if not user:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
                return

            if user.password != password:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
                return

            QMessageBox.information(
                self,
                "Успех",
                f"Добро пожаловать, {user.name}!",
            )
            self.current_user = user
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            session.close()

    def get_current_user(self):
        return self.current_user


class Register(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 380)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title_label = QLabel("Регистрация")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        form_layout = QFormLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setMinimumSize(200, 30)
        self.username_edit.setPlaceholderText("Введите имя пользователя")
        form_layout.addRow("Имя пользователя:", self.username_edit)

        self.email_edit = QLineEdit()
        self.email_edit.setMinimumSize(200, 30)
        self.email_edit.setPlaceholderText("example@mail.com")
        form_layout.addRow("Email:", self.email_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumSize(200, 30)
        self.password_edit.setPlaceholderText("Минимум 8 символов")
        form_layout.addRow("Пароль:", self.password_edit)

        self.password_confirm_edit = QLineEdit()
        self.password_confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirm_edit.setMinimumSize(200, 30)
        self.password_confirm_edit.setPlaceholderText("Повторите пароль")
        form_layout.addRow("Повторите пароль:", self.password_confirm_edit)

        layout.addLayout(form_layout)

        login_label = QLabel('<a href="login">Есть аккаунт? Войти...</a>')
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_label.linkActivated.connect(self.show_login)
        layout.addWidget(login_label)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
        )
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def show_login(self):
        self.reject()
        login_dialog = Login(self.parent())
        login_dialog.exec()

    def validate_and_accept(self):
        username = self.username_edit.text().strip()
        email = self.email_edit.text().strip()
        password = self.password_edit.text()
        password_confirm = self.password_confirm_edit.text()

        if not all([username, email, password, password_confirm]):
            QMessageBox.warning(
                self,
                "Ошибка",
                "Все поля должны быть заполнены!",
            )
            return

        if password != password_confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        session = Session()

        try:
            existing_user = (
                session.query(User)
                .filter((User.name == username) | (User.email == email))
                .first()
            )

            if existing_user:
                if existing_user.name == username:
                    QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Пользователь с таким именем уже существует!",
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Пользователь с таким email уже существует!",
                    )
                return

            new_user = User(name=username, email=email, password=password)
            session.add(new_user)
            session.commit()

            QMessageBox.information(
                self,
                "Успех",
                "Регистрация прошла успешно!",
            )
            self.accept()

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка валидации", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            session.rollback()
        finally:
            session.close()
