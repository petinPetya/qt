button_cap_style = """
  padding: 10px;
  background-color: #6f00ff;
  color: #fff;
  width: 8px;
  height: 6px;
  border: 1px solid black;
  border-radius: 1px;
  font-size: 16px;
  cursor: pointer;
  margin: 1px;
"""

button_cap_style_hover = """
  background-color: #722eb2;
  transform: translateY(-1px);
"""

text_style_title = """
  font: 3em Georgia, bold;
  color: #1d073d;
  background-color: #d3ccd8;
"""

container_style = """
  background-color: #ffffff;
  border: 1px solid #d0d0d0;
  border-radius: 3px;
"""

filter_button_style = """
  QPushButton {
      background-color: #6c757d;
      color: white;
      border: none;
      border-radius: 3px;
      font-size: 9px;
      font-weight: bold;
  }
  QPushButton:hover {
      background-color: #5a6268;
      border: 1px solid #545b62;
  }
  QPushButton:pressed {
      background-color: #545b62;
      padding: 1px 0px 0px 1px;
  }
"""


"""
{% extends "base.html" %}
<body>
    {% block kot %}
    <div class="container">
        <form method="post" class="feedback-form">
            {% csrf_token %}
            
            <h2 class="form-title">Форма обратной связи</h2>
            <!-- Цикл по видимым полям формы -->
            {% for field in form.visible_fields %}
                <div class="mb-3 {% if field.field.required %}required{% endif %}">
                    <label for="{{ field.id_for_label }}" class="form-label">
                        {{ field.label }}
                        {% if field.field.required %}<span class="text-danger">*</span>{% endif %}
                    </label>
                    
                    <!-- Поле ввода -->
                    {{ field }}
                    
                    <!-- Подсказка (help text) -->
                    {% if field.help_text %}
                        <div class="form-text">{{ field.help_text }}</div>
                    {% endif %}
                    
                    <!-- Ошибки поля -->
                    {% if field.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in field.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}

            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button type="reset" class="btn btn-outline-secondary me-md-2">Очистить</button>
                <button type="submit" class="btn btn-primary">Отправить</button>
            </div>
        </form>
    </div>

    <!-- Стили для полей формы -->
    <style>
        .feedback-form .form-control {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 12px 15px;
            font-size: 16px;
            transition: all 0.3s ease;
            width: 100%;
        }

        .feedback-form .form-control:focus {
            border-color: #007bff;
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }

        .feedback-form .required .form-label {
            font-weight: 600;
        }

        .feedback-form textarea.form-control {
            resize: vertical;
            min-height: 120px;
        }

        .feedback-form .form-title {
            color: #343a40;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 700;
        }

        .feedback-form {
            max-width: 600px;
            margin: 0 auto;
            padding: 30px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    {% endblock %}
</body>
</html>
"""
