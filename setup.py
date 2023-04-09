
from setuptools import setup, find_packages


version = '1.0.0'
url = 'https://github.com/pmaigutyak/mp-tags'


setup(
    name='django-mp-tags',
    version=version,
    description='Django tags apps',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
