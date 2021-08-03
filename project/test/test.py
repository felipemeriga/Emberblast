from unittest import TestCase

HAS_ATTR_MESSAGE = '{} should have an attribute {}'


class BaseTestCase(TestCase):

    # def setUp(self):
    #     create_dynamic_jobs()
    #     create_dynamic_races()
    #     print(dynamic_jobs_classes)

    def assertHasAttr(self, obj, attrname, message=None):
        if not hasattr(obj, attrname):
            if message is not None:
                self.fail(message)
            else:
                self.fail(HAS_ATTR_MESSAGE.format(obj, attrname))