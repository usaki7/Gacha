from setuptools import setup, find_packages

setup(
    name='gacha_app',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow>=9.0.0'
    ],
    entry_points={
        'console_scripts': [
            'gacha = gacha_app.main:main'
        ],
    },
    package_data={
        'gacha_app': ['config.json', 'images/*']
    },
    author='',
    description='Python 本地扭蛋机应用'
)
