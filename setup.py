import setuptools
from mailerlite_extensions.version import Version

PACKAGES = setuptools.find_packages(exclude=[
    'tests'
])

setuptools.setup(name='mailerlite_extensions',
                 version=Version('1.0.0').number,
                 description='Mailerlite extensions for Python',
                 long_description=open('README.md').read().strip(),
                 author='Kyle Shovan',
                 author_email='kyle@codebykyle.com',
                 url='https://github.com/codebykyle/mailerlite_extensions',
                 packages=PACKAGES,
                 install_requires=[
                     'mailerlite'
                 ],
                 license='MIT License',
                 zip_safe=False,
                 keywords='mailerlite',
                 classifiers=[
                     'Packages',
                     'Mailerlite'
                 ])
