from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from tasks.models import Task
from users.models import User


class TaskModelTest(TestCase):
    def setUp(self) -> None:
        self.user_valid = User.objects.create_user(username="João", password="João123")
        self.example_task = Task.objects.create(
            title="Example Task", description="Task description", user=self.user_valid
        )
        self.other_task = Task.objects.create(
            title="Other Task", user=self.user_valid
        )

    def test_title_empty_validation(self) -> None:
        task = Task(title="    ")
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_title_blank_validation(self) -> None:
        task = Task(title="")
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_valid_title(self) -> None:
        self.example_task.full_clean()

    def test_unique_title(self) -> None:
        with self.assertRaises(IntegrityError):
            Task.objects.create(title="Example Task")

    def test_title_max_length(self) -> None:
        long_title = "a" * 256
        task = Task(title=long_title)
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_long_description(self) -> None:
        long_description = "a" * 1000
        task = Task.objects.create(
            title="Valid Title", description=long_description, user=self.user_valid
        )
        self.assertEqual(task.description, long_description)

    def test_task_valid(self) -> None:
        self.assertEqual(self.example_task.title, "Example Task")
        self.assertEqual(self.example_task.description, "Task description")
        self.assertFalse(self.example_task.is_completed)

    def test_task_updated_with_spaces_in_description(self) -> None:
        self.other_task.description = "   "
        self.other_task.save()
        self.assertEqual(self.other_task.description, "")

    def test_task_update_with_none_description(self) -> None:
        self.other_task.description = None  # type: ignore
        self.other_task.save()
        self.assertEqual(self.other_task.description, "")

    def test_toggle_is_completed_update(self) -> None:
        self.assertFalse(self.example_task.is_completed)  # verifica o valor padrão
        self.example_task.is_completed = True
        self.example_task.save()
        self.assertTrue(self.example_task.is_completed)
        self.example_task.is_completed = False
        self.example_task.save()
        self.assertFalse(self.example_task.is_completed)

    def test_created_at_is_set_and_updated_at_is_initially_equal(self) -> None:
        self.assertIsNotNone(self.example_task.created_at)
        self.assertIsInstance(self.example_task.created_at, datetime)
        self.assertAlmostEqual(
            self.example_task.updated_at,
            self.example_task.created_at,
            delta=timedelta(seconds=1),
        )

    def test_created_at_does_not_change_on_update(self) -> None:
        initial_created_at = self.other_task.created_at
        self.other_task.title = "New Title"
        self.other_task.save()
        self.assertEqual(self.other_task.created_at, initial_created_at)
        self.assertIsInstance(self.other_task.created_at, datetime)

    def test_updated_at_is_set_on_update(self) -> None:
        initial_updated_at = self.example_task.updated_at
        self.example_task.title = "Updated Test Task"
        self.example_task.save()
        self.assertGreater(self.example_task.updated_at, initial_updated_at)
