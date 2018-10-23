import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cspy",
    version="0.0.1",
    author="Avikor",
    author_email="44028161+avikor@users.noreply.github.com",
    description="A small package for solving finite constraint satisfaction problems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avikor/constraint_satisfaction_problems",
    packages=setuptools.find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Programming Language :: Python :: 3.5.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
