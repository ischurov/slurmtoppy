from setuptools import setup, find_packages

setup(
    name="slurmtoppy",
    version="0.1.5",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "slurmtop=slurmtoppy.main:run",  # Point to a function that starts your app
        ],
    },
    author="Ilya V. Schurov",
    author_email="ilya@schurov.com",
    description="A console-based SLURM job monitoring tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ischurov/slurmtoppy",  # Replace with your own GitHub URL
    license="MIT",  # Or whichever license you choose
    classifiers=[
        # Classifiers help users find your project
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        # List your project's dependencies here
        # e.g., 'requests>=2.22.0'
    ],
)
