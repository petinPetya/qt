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
__all__ = "TestsOFForm"

import os
from pathlib import Path
import tempfile

from django.test import TestCase, Client
from django.urls import reverse

from feedback.forms import FeedbackForm


class TestsOFForm(TestCase):
    def setUp(self):
        self.client = Client()

    def test_form_in(self):
        response = self.client.get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_form_labels_and_help_text(self):
        form = FeedbackForm()
        self.assertEqual(form.fields["name"].label, "Имя")
        self.assertEqual(form.fields["mail"].label, "Почта")
        self.assertEqual(form.fields["text"].label, "Текстовое поле")

    def test_form_submission_redirect(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)

                data = {
                    "name": "Test User",
                    "mail": "test@example.com",
                    "text": "Test message content",
                }

                response = self.client.post(
                    reverse("homepage:home"),
                    data,
                    follow=True,
                )
                self.assertEqual(response.status_code, 200)

            finally:
                os.chdir(original_cwd)

    def test_email_file_creation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)
                mail_dir = Path("feedback/send_mail")
                mail_dir.mkdir(parents=True, exist_ok=True)

                data = {
                    "name": "Test User",
                    "mail": "test@example.com",
                    "text": "Test message content from form",
                }

                self.client.post(reverse("feedback:feedback"), data)
                self.assertTrue(os.path.exists("feedback/send_mail"))
                files = os.listdir("feedback/send_mail")
                self.assertEqual(len(files), 1)
                filepath = Path("feedback/send_mail") / files[0]
                with filepath.open("r", encoding="utf-8") as f:
                    content = f.read()
                    self.assertIn("Test message content from form", content)
                    self.assertIn("test@example.com", content)

            finally:
                os.chdir(original_cwd)

    def test_feedback_form_status_ok_on_invalid_data(self):
        invalid_data = {"name": "", "text": "", "mail": "invalid"}
        response = self.client.post(
            reverse("feedback:feedback"),
            data=invalid_data,
        )
        self.assertEqual(response.status_code, 200)

    def test_feedback_form_has_errors(self):
        invalid_data = {"name": "", "text": "", "mail": "invalid"}
        response = self.client.post(
            reverse("feedback:feedback"),
            data=invalid_data,
        )
        form = response.context["form"]
        self.assertTrue(form.errors)

    def test_feedback_form_error_fields(self):
        invalid_data = {"name": "", "text": "", "mail": "invalid"}
        response = self.client.post(
            reverse("feedback:feedback"),
            data=invalid_data,
        )
        form = response.context["form"]
        self.assertIn("name", form.errors)
        self.assertIn("text", form.errors)
        self.assertIn("mail", form.errors)
"""
