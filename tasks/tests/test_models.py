from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from tasks.models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.example_task = Task.objects.create(
            title='Example Task', description='Task description'
        )
        self.other_task = Task.objects.create(
            title='Other Task'
        )

    def test_title_empty_validation(self):
        task = Task(title='    ')
        with self.assertRaises(ValidationError):
            task.full_clean()
        
    def test_title_blank_validation(self):
        task = Task(title='')
        with self.assertRaises(ValidationError):
            task.full_clean()
        
    def test_valid_title(self):
        self.example_task.full_clean()
            
    def test_unique_title(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(title='Example Task')
            
    def test_title_max_length(self):
        long_title = "a" * 256
        task = Task(title=long_title)
        with self.assertRaises(ValidationError):
            task.full_clean()
    
    def test_long_description(self):
        long_description = "a" * 1000
        task = Task.objects.create(title="Valid Title", description=long_description)
        self.assertEqual(task.description, long_description)
    
    def test_task_valid(self):
        self.assertEqual(self.example_task.title, 'Example Task')
        self.assertEqual(self.example_task.description, 'Task description')
        self.assertFalse(self.example_task.is_completed)
    
    def test_task_updated_with_spaces_in_description(self):
        self.other_task.description = '   '
        self.other_task.save()
        self.assertEqual(self.other_task.description, '')
    
    def test_task_update_with_none_description(self):
        self.other_task.description = None # type: ignore
        self.other_task.save()
        self.assertEqual(self.other_task.description, '')
    
    def test_toggle_is_completed_update(self):
        self.assertFalse(self.example_task.is_completed) # verifica o valor padrão
        self.example_task.is_completed = True
        self.example_task.save()
        self.assertTrue(self.example_task.is_completed)
        self.example_task.is_completed = False
        self.example_task.save()
        self.assertFalse(self.example_task.is_completed)
        
    def test_created_at_is_set_and_updated_at_is_initially_equal(self):
        self.assertIsNotNone(self.example_task.created_at)
        self.assertIsInstance(self.example_task.created_at, datetime)
        self.assertAlmostEqual(self.example_task.updated_at, self.example_task.created_at, delta=timedelta(seconds=1))
        
    def test_created_at_does_not_change_on_update(self):
        initial_created_at = self.other_task.created_at
        self.other_task.title = 'New Title'
        self.other_task.save()
        self.assertEqual(self.other_task.created_at, initial_created_at)
        self.assertIsInstance(self.other_task.created_at, datetime)
        
    def test_updated_at_is_set_on_update(self):
        initial_updated_at = self.example_task.updated_at
        self.example_task.title = 'Updated Test Task'
        self.example_task.save()
        self.assertGreater(self.example_task.updated_at, initial_updated_at)
