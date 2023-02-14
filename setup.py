import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    README = fh.read()

setuptools.setup(
    name="python-podcastindex",
    version="1.10.0",
    description="A python wrapper for the Podcast Index API (podcastindex.org).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SarvagyaVaish/python-podcastindex",
    author="Sarvagya (Survy) Vaish",
    author_email="sarvagya.vaish7@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["podcastindex"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "realpython=podcastindex.__main__:main",
        ]
    },
    python_requires=">=2.7",
)
