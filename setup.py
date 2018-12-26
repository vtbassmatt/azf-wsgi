import setuptools

setuptools.setup(
    name='azf-wsgi',
    version='0.1',
    description='Azure Functions WSGI implementation',
    long_description='Adapts the Azure Functions API to speak WSGI. Projects in Django, Flask, and other web frameworks simply drop right in to Azure Functions.',
    author='Matt Cooper',
    author_email='vtbassmatt@gmail.com',
    url='https://github.com/vtbassmatt/azf-wsgi',
    packages=setuptools.find_packages(),
    install_requires=['azure-functions'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
    ]
)