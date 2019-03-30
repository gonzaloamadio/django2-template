"""
Create some very useful utilities for future tests: creating test-users in bulk,
logging a user in, finding specific text in the html, and debugging.

In the case of multiple types of profiles. Create a function for each one.

DEPENDS ON TEST:  *nothing* (must not depend on any test_*.py file)
DEPENDED ON TEST: test__profile.py

--- Generic information on running tests ---

To run a single test:
    python -Wall manage.py test path.to.test__file_name

To run all tests:
    python -Wall manage.py test name.of.app

Running tests documentation:
- https://docs.djangoproject.com/en/1.7/topics/testing/overview/#running-tests

Information on '-Wall' is at the bottom of that same section. If the
output is too verbose, try it again without '-Wall'.

If a test fails because the test database cannot be created, grant your
database user creation privileges:
- http://dba.stackexchange.com/questions/33285/how-to-i-grant-a-user-account-permission-to-create-databases-in-postgresql  # noqa: E501
"""

import factory
from django.contrib.auth.models import User

from auth_lifecycle.models import UserProfile

from .models import MIN_BIRTH_YEAR

TEST_USER_COUNT = 5
"""The number of test users to create. Equal to `5`."""
TEST_PASSWORD = 'password123abc'
"""The password shared by all test users. Equal to `'password123abc'`."""


class UserProfileFactory(factory.django.DjangoModelFactory):
    """
    Creates `UserProfile`-s, where each user has a unique birth year,
    starting with <link to .models.MIN_BIRTH_YEAR>.

    *Warning*: Creating more than
        MAX_BIRTH_YEAR - MIN_BIRTH_YEAR
     users will cause a ValidationError.
    """

    # Uncommenting this line would allow you to directly create a
    # UserProfile, which would then automatically create a User.
    # - Docs: http://factoryboy.readthedocs.org/en/latest/reference.html#subfactory
    # user = factory.SubFactory('auth_lifecycle.test__utilities.UserFactory', profile=None)
    class Meta:
        model = UserProfile

    # factory.Sequence always starts at one. This starts it at
    # MIN_BIRTH_YEAR.
    # http://factoryboy.readthedocs.org/en/latest/reference.html#sequence
    # http://stackoverflow.com/questions/15402256/how-to-pass-in-a-starting-sequence-number-to-a-django-factoryboy-factory
    birth_year = factory.Sequence(lambda n: n + MIN_BIRTH_YEAR - 1)


class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates `User`-s and its corresponding `UserProfile`-s. Each user has
    the same attributes, but with a unique sequence number, starting with
    one.

    See <link to TEST_PASSWORD>.
    """

    class Meta:
        model = User

    # Automatically create a profile when the User is created.
    # - Docs:
    # http://factoryboy.readthedocs.org/en/latest/reference.html?highlight=subfactory#relatedfactory  # noqa: E501
    profile = factory.RelatedFactory(UserProfileFactory, 'user')

    username = factory.Sequence(lambda n: 'test_username{}'.format(n))
    first_name = factory.Sequence(lambda n: 'test_first_name{}'.format(n))
    last_name = factory.Sequence(lambda n: 'test_last_name{}'.format(n))
    email = factory.Sequence(lambda n: 'test_email{}@example.com'.format(n))

    # http://factoryboy.readthedocs.org/en/latest/reference.html#postgenerationmethodcall
    # See Django mention at the bottom of that documentation section.
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)


def create_insert_test_users():
    """
    Insert <link to TEST_USER_COUNT> test users into the database. I don't
    understand why, but even though this is called for every test, via
    `setUp`, this does *not* create more than `TEST_USER_COUNT` users.
    Use the debugging statements to prove this.
    """

    # print('a User.objects.count()=' + str(User.objects.count()))

    # http://factoryboy.readthedocs.org/en/latest/reference.html?highlight=create#factory.create_batch
    UserFactory.create_batch(TEST_USER_COUNT)

    # print('b User.objects.count()=' + str(User.objects.count()))


def login_get_next_user(test_instance):
    """
    Log in the next test user, assert it succeeded, and return the `User`
    object.
    """
    test_instance.client.logout()

    test_user = UserFactory()
    # debug_test_user(test_user, prefix='Attempting to login:')

    did_login_succeed = test_instance.client.login(
        username=test_user.username, password=TEST_PASSWORD
    )
    test_instance.assertTrue(did_login_succeed)

    return test_user


def assert_attr_val_in_content(
    #test_instance, attribute_name, expected_value, page_content_str
    test_instance, expected_value, page_content_str
):
    """A specific attribute should be somewhere in the html."""
    # print('assert_attr_val_in_content: expected_value=' + expected_value)
    test_instance.assertTrue(str(expected_value) in page_content_str)


def debug_test_user(test_user, prefix=''):
    """
    Print all user attributes to standard out, except password.

    Parameters:
    - prefix: Defaults to `''`. If not the empty string, printed before
    the user information
    """
    if prefix is not '':
        print(prefix)

    profile = test_user.profile
    print('test_user.id=' + str(test_user.id))
    print('   username=' + test_user.username + ', password=' + TEST_PASSWORD)
    print(
        '   first_name=' + test_user.first_name + ', last_name=' + test_user.last_name
    )
    print('   email=' + test_user.email)
    print('   profile=' + str(profile))
    print('      profile.birth_year=' + str(profile.birth_year))
