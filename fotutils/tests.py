from django.core.exceptions import ValidationError
from django.test import TestCase


class ModelTestHelper(TestCase):
    """Base class with helper methods for test models."""
    model = None  # Model to use, this must be specified in subclasses

    def check_save_validation(self, obj, field_name, error_key='blank'):
        """
        Checks for raise Empty field Validation exception on save model.

        :param obj: Object to save
        :param field_name: Model attribute to check empty
        :param error_key: Key in error message, set None for 'blank' key (default: 'blank')
        """
        if error_key == 'unique':
            exception_message = "{'%s': [u'%s with this %s already exists.']}" % (
                field_name, obj.__class__.__name__, field_name.capitalize()
            )
        else:
            if error_key is None:
                error_key = 'blank'
            exception_message = "{'%s': [u'This field cannot be %s.']}" % (field_name, error_key)
        with self.assertRaisesMessage(ValidationError, exception_message):
            obj.full_clean()
            obj.save()

    def check_require_field(self, required_field='slug', error_key=None, **kwargs):
        """
        Checks if a model with a required field is working as expected.

        :param required_field: Field name to check for require checks
        :param error_key: String key to identify the error in validation exception, see this parameter in
            :method:`fotutils.ModelTestHelper.check_save_validation` (default: None)
        :param kwargs: Parameters for model creation
        """
        obj = self.model(**kwargs)
        self.check_save_validation(obj, required_field, error_key)

    def check_unique_field(self, unique_field='slug', obj1_dict=None, obj2_dict=None, check_value='unique-val'):
        """
        Checks if a model unique field is working as expected by saving to object with field repeated value.

        :param unique_field: Field name to check for unique
        :param obj1_dict: Serialized first object dictionary with required fields except for unique_field
        :param obj2_dict: Serialized second object dictionary with required fields except for unique_field
        :param check_value: Allow to specify a value for unique field, used for non string field value
            (default: 'unique-val')
        """
        if not obj1_dict:
            obj1_dict = {}
        if not obj2_dict:
            obj2_dict = {}
        obj1_dict[unique_field] = check_value
        obj1 = self.model(**obj1_dict)
        obj1.save()
        self.assertEqual(self.model.objects.count(), 1)
        obj2_dict[unique_field] = check_value
        obj2 = self.model(**obj2_dict)
        # On save object 2 raise a validation exception
        self.check_save_validation(obj2, unique_field, 'unique')

    def check_saving_and_retrieving_objects(self, obj1_dict=None, obj2_dict=None):
        """
        Checks if two objects of a model can be saved and retrieved from database.

        :param obj1_dict: Serialized first object dictionary, each key in dictionary must be an object's field
        :param obj2_dict: Serialized second object dictionary, each key in dictionary must be an object's field
        """
        if not obj1_dict:
            obj1_dict = {}
        if not obj2_dict:
            obj2_dict = {}
        self.model.objects.create(**obj1_dict)
        self.model.objects.create(**obj2_dict)

        saved_objects = self.model.objects.all()
        self.assertEqual(saved_objects.count(), 2)

        save_obj1 = saved_objects[0]
        save_obj2 = saved_objects[1]
        main_key = obj1_dict.keys()[0]
        self.assertEqual(getattr(save_obj1, main_key), obj1_dict[main_key])
        self.assertEqual(getattr(save_obj2, main_key), obj2_dict[main_key])

    def check_string_representation(self, result, **kwargs):
        """
        Checks for model string representation.

        :param result: Expected text for model string representation
        :param kwargs: Params for Model creation
        """

        obj = self.model.objects.create(**kwargs)
        self.assertEqual(str(obj), result)
