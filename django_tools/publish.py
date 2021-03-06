from pathlib import Path

from creole.setup_utils import assert_rst_readme, update_rst_readme
from poetry_publish.publish import poetry_publish
from poetry_publish.utils.subprocess_utils import verbose_check_call

import django_tools


PACKAGE_ROOT = Path(django_tools.__file__).parent.parent


def update_readme():
    return update_rst_readme(
        package_root=PACKAGE_ROOT,
        filename='README.creole'
    )


def publish():
    """
        Publish python-creole to PyPi
        Call this via:
            $ poetry run publish
    """
    # don't publish if README is not up-to-date:
    assert_rst_readme(package_root=PACKAGE_ROOT, filename='README.creole')

    # don't publish if code style wrong:
    verbose_check_call('make', 'fix-code-style')

    poetry_publish(
        package_root=PACKAGE_ROOT,
        version=django_tools.__version__,
        creole_readme=True  # don't publish if README.rst is not up-to-date
    )
