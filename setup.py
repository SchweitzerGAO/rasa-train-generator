from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rasa_gen",
    version="0.0.1",
    keywords=["pip", "rasa_gen"],
    description="Rasa train data generator",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT License",
    url="https://github.com/SchweitzerGAO/rasa-train-generator",
    author="Charles Gao",
    author_email="charlesgao2101024@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['cn2an']
)
