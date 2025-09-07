from setuptools import setup, find_packages

with open("README_EN.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="monowidget",
    version="1.0.0",
    author="MonoWidget Team",
    author_email="monowidget@example.com",
    description="A Python tool for creating and managing parameter interfaces with automatic visual component generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EagleBaby/monowidget",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.4.0",
    ],
    include_package_data=True,
    zip_safe=False,
)