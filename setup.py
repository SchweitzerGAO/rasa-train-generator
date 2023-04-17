from setuptools import setup, find_packages

setup(
    name="rasa_gen",  # 这里是pip项目发布的名称
    version="0.0.1",  # 版本号，数值大的会优先被pip
    keywords=["pip", "rasa_gen"],  # 关键字
    description="Rasa train data generator",
    long_description="Rasa train data generator version 0.0.1",
    license="MIT Licence",  # 许可证

    url="https://github.com/Adenialzz/SongUtils",  # 项目相关文件地址，一般是github项目地址即可
    author="A",  # 作者
    author_email="********@***.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
)
