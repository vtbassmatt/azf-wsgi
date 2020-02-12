import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='azf-wsgi',
    version='0.3.1',
    description='Azure Functions WSGI implementation [deprecated]',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Matt Cooper',
    author_email='vtbassmatt@gmail.com',
    url='https://github.com/vtbassmatt/azf-wsgi',
    packages=setuptools.find_packages(),
    install_requires=['azure-functions'],
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
    ]
)
