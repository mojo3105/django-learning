from django.test import TestCase
from django.utils import timezone
from .models import SalesMan

class SalesManModelTest(TestCase):
    def test_create_salesman(self):
        # Create a SalesMan object
        salesman = SalesMan.objects.create(
            name='John Doe'.strip(),
            email=''.strip(),
            phone_no=1234567890,
            address='123 Main St'.strip(),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        # Check if the object was created successfully
        self.assertEqual(salesman.name, 'John Doe')
        self.assertEqual(salesman.email, 'johndoe@example.com')
        self.assertEqual(salesman.phone_no, 1234567890)
        self.assertEqual(salesman.address, '123 Main St')
        self.assertIsNotNone(salesman.created_at)
        self.assertIsNotNone(salesman.updated_at)
