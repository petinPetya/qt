import sqlalchemy
from sqlalchemy.orm import validates

db = sqlalchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    name_normalized = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=True, nullable=False)
    description_length = db.Column(db.Integer, primary_key=True, default=70)

    @validates("password")
    def checkPassword(self, key, password):
        print(password)
        print("\n============\n")
        if len(password) < 8:
            raise ValueError("Пароль слишком короткий!")
        return password

    @validates("name")
    def checkName(self, key, name):
        print(name)
        print("\n=========\n")
        if not name[0].isalnum():
            raise ValueError("Имя должно начинаться с буквы!")
        return name

    def __repr__(self):
        return f"id: {self.id}\nname: {self.name}\npassword: {self.password}"
