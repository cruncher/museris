from setuptools import setup, find_packages
setup(
    name='museris-data',
    version='0.1',
    description='Data models and scraper for https://museris.lausanne.ch/',
    author='Cruncher',
    author_email='marco@cruncher.ch',
    url='https://github.com/cruncher/museris',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >= 1.7',
        'beautifulsoup4 >= 4.3.2',
        'progress >= 1.2',
        'requests >= 2.5.1'
    ]
)
