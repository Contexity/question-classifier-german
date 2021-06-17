import setuptools

setuptools.setup(name="NLP Server Interface",
version='0.2',
description='The interface of the nlp server',
url='#',
author='Contexity AG',
install_requires=['connexion','connexion[swagger-ui]'],
author_email='',
packages=setuptools.find_packages(),
include_package_data=True,
zip_safe=False)