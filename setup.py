from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='ebay_multilocation_item_finder',
    version='0.0.1',
    url='https://github.com/dalepotter/ebay-multilocation-item-finder',
    author='Dale Potter',
    author_email='dalepotter@gmail.com',
    description='Search the ebay API to find items located close to a set of postcodes.',
    packages=find_packages(),
    install_requires=[
        "ebaysdk==2.1.5",
        "emails==0.5.15",
        "Jinja2==2.10"
    ]
)
