from setuptools import setup
from version import get_git_version

# From http://bugs.python.org/issue15881
try:
    import multiprocessing
except ImportError:
    pass

from io import open

with open('requirements.txt', encoding='utf-8') as requirements:
    requires = [l.strip() for l in requirements]

with open('README.md', encoding='utf-8') as readme_f:
    readme = readme_f.read()

setup(
    name='Webflowpy',
    version=get_git_version(),
    packages=['webflowpy'],
    url='https://github.com/rfechtner/webflowpy',
    license='MIT License',
    author='Ron Fechtner',
    author_email='ronfechtner@gmail.com',
    description='Python Webflow CMS API Client',
    long_description=readme,
    install_requires=requires
)
