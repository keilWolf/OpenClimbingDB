import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="climbing-crawler",
    version="0.0.1",
    author="Wolfram Keil",
    author_email="wkeildev@gmail.com",
    description="A web scraping project to get data for the OpenClimbingDatabase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keilWolf/ClimbingCrawler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
