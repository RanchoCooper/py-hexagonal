"""
Setup script for py-hexagonal.
"""

from setuptools import find_packages, setup

setup(
    name="py-hexagonal",
    version="0.1.0",
    description="Python Hexagonal Architecture Template",
    author="",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.3.3",
        "Flask-RESTful>=0.3.10",
        "Flask-Cors>=4.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.3",
        "redis>=4.6.0",
        "SQLAlchemy>=2.0.20",
    ],
    python_requires=">=3.9",
) 