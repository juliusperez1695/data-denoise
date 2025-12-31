from setuptools import setup, find_packages

setup(
    # This setup.py is primarily for backward compatibility.
    # Configuration is read from pyproject.toml.
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)

if __name__ == "__main__":
    setup()