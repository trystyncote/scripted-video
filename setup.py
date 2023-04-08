from setuptools import setup  # , find_packages

if __name__ == "__main__":
    setup(
        extras_require={
            "testing": [
                "pytest>=6.0",
                "pytest-cov>=2.0",
                "mypy>=0.910",
                "flake8>=3.9",
                "tox>=3.24",
            ],
        },
    )