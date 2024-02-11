import setuptools
from mailerlite_extensions.version import Version


setuptools.setup(name='mailerlite_extensions',
                 version=Version('1.0.0').number,
                 description='Mailerlite extensions for Python',
                 long_description=open('README.md').read().strip(),
                 author='Kyle Shovan',
                 author_email='kyle@codebykyle.com',
                 url='https://github.com/codebykyle/mailerlite_extensions',
                 py_modules=['mailerlite_extensions'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='mailerlite',
                 classifiers=[
                     'Packages',
                     'Mailerlite'
                 ])
