from setuptools import setup, find_packages

setup(
    name='gacha_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow>=9.0.0'
    ],
    entry_points={
        'console_scripts': [
            'gacha = gacha_app:main'
        ],
    },
    package_data={
        'gacha_app': ['config/*.json', 'resources/images/*']
    },
    author='',
    description='Python 本地扭蛋机应用',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Games/Entertainment',
    ],
)
