from setuptools.command.test import test as TestCommand

DIR = ''


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--assert=plain'] + \
            [DIR + x for x in os.listdir(DIR)
             if x.endswith('.py') and x[0] not in '._']

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)
