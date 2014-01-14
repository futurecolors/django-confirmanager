from os import path
import codecs
from setuptools import setup, find_packages

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


setup(
    name='django-confirmanager',
    version='0.3',
    author='Ilya Baryshev',
    author_email='baryshev@gmail.com',
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    url='https://github.com/futurecolors/django-confirmanager',
    license='MIT',
    description="Simple email confirmation application.",
    long_description=read(path.join(path.dirname(__file__), 'README.rst')),
    install_requires=[
        'django-templated-email>=0.4.7,<0.5',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
