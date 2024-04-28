from setuptools import setup, find_packages

setup(
    name='pytest-report-plugin',
    version='1.0.0',
    author='Shaik Faizan Roshan Ali',
    author_email='roshan.shaik.ml@gmail.com',
    description='A pytest plugin for reporting test execution progress and results',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/roshan-shaik-ml/pytest-report-plugin',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'pytest',
        'requests',
        'hypothesis',
    ],
    entry_points={
        'pytest11': [
            'report_plugin = pytest_report_plugin.plugin',
        ],
    },
)
