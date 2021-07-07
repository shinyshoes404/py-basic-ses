from setuptools import setup

setup(
    name='py-basic-ses',
    version='0.1.0',    
    description="A simple python command line application and library to help send emails via Amazon Web Services' Simple Email Service, or AWS SES.",
    url='https://github.com/shinyshoes404/py-basic-ses',
    author='shinyshoes',
    author_email='shinyshoes404@protonmail.com',
    license='MIT License',
    packages=['py_basic_ses'],
    package_dir={'':'src'},
    entry_points = { 'console_scripts' : ['send-test=py_basic_ses.entry:send_test_email',
                    'send-email=py_basic_ses.entry:send_email']},
    install_requires=[
        'boto3>=1.17',
        'click'
    
    ],

    python_requires = '>=3.8.*,!=3.10.*',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',           
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)