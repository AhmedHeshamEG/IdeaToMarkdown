from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="idea-to-markdown",
    version="0.1.0",
    author="Idea to Markdown Contributors",
    author_email="maintainers@example.com",
    description="A voice-first AI agent for capturing ideas into Markdown files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AhmedHeshamEG/IdeaToMarkdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.0.0",
        "openai>=1.5.0",
        "pyaudio>=0.2.13",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "flake8>=6.0.0",
            "black>=23.3.0",
            "mypy>=1.3.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "idea-to-markdown=idea_to_markdown.main:main",
        ],
    },
)
