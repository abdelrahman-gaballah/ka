from setuptools import setup, find_packages
from pathlib import Path

readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else "Ka - Easy Linux Commands for beginners"

setup(
    name="ka-linux-commands",
    version="0.1.0",
    author="Abdelrahman Gaballah",
    author_email="abdelrahman.gaballah.official@outlook.com",
    description="Easy Linux Commands - Natural language shortcuts for Linux terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abdelrahman-gaballah/ka",
    project_urls={
        "Bug Reports": "https://github.com/abdelrahman-gaballah/ka/issues",
        "Source": "https://github.com/abdelrahman-gaballah/ka",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ka=core.cli:main",
        ],
    },
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
        "translation": ["googletrans==4.0.0rc1"],
        "ascii": ["pyfiglet>=0.8.post1"],
    },
    package_data={
        "": ["langs/*.json", "user/*.json", "config.json"],
    },
    data_files=[
        ("share/doc/ka", ["README.md", "LICENSE"]),
    ],
    zip_safe=False,
)
