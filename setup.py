
from setuptools import setup, find_packages

setup(
    name='umuus_template_cli',
    description='A package.',
    long_description=('A package.\n'
 '\n'
 'umuus-template-cli\n'
 '==================\n'
 '\n'
 'Installation\n'
 '------------\n'
 '\n'
 '    $ pip install umuus_template_cli\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    $ umuus_template_cli\n'
 '\n'
 '    >>> import umuus_template_cli\n'
 '\n'
 'Authors\n'
 '-------\n'
 '\n'
 '- Jun Makii <junmakii@gmail.com>\n'
 '\n'
 'License\n'
 '-------\n'
 '\n'
 'GPLv3 <https://www.gnu.org/licenses/>'),
    py_modules=['umuus_template_cli'],
    version='0.1',
    url='https://github.com/junmakii/umuus-template-cli',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['PyYAML', 'jinja2', 'addict', 'git://github.com/junmakii/umuus_dict_util.git#egg=umuus_dict_util'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Natural Language :: English', 'Programming Language :: Python', 'Programming Language :: Python :: 3'],
    entry_points={'console_scripts': ['umuus_template_cli = umuus_template_cli:main']}
)

