from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='ebay_multilocation_item_notifier',
    version='0.0.1',
    url='https://github.com/dalepotter/ebay_multilocation_item_notifier',
    author='Dale Potter',
    author_email='dalepotter@gmail.com',
    description='Search the ebay API to find items located close to a set of postcodes.',
    packages=find_packages(),
    install_requires=[
        "ebaysdk>=2.2.0",
        "emails==0.6.0",
        "Jinja2==3.0.3"
    ]
)
