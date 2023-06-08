from django.test import TestCase
from .models import User

# Create your tests here.

class UserModelTest(TestCase):
  def setUpTestData():
    # Set up non-modified objects used by all test methods
    User.objects.create(
      name = 'Bob Kustow',
      username = 'babybobby123',
      email = 'babybobby123@email.com'
    )

  def test_user_name(self):
    # Get an user object to test
    user = User.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its data
    field_label = user._meta.get_field('name').verbose_name

    # Compare the value to the expected result
    self.assertEqual(field_label, 'name')

  def test_user_name_max_length(self):
    # Get a user object to test
    user = User.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its max_length
    max_length = user._meta.get_field('name').max_length

    # Compare the value to the expected result i.e. 50
    self.assertEqual(max_length, 50)