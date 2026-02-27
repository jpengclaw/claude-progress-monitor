from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-progress-monitor",
    version="1.0.0",
    author="Operational Neural Network",
    author_email="noreply@operationalneural.network",
    description="Automatic progress monitoring for Claude subagent execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpengclaw/claude-progress-monitor",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies for core functionality
        # User can install anthropic separately if needed
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "anthropic": [
            "anthropic>=0.8",
        ],
    },
    keywords="claude ai subagent monitoring progress tracking async",
    project_urls={
        "Bug Reports": "https://github.com/jpengclaw/claude-progress-monitor/issues",
        "Source": "https://github.com/jpengclaw/claude-progress-monitor",
        "Documentation": "https://github.com/jpengclaw/claude-progress-monitor#readme",
    },
)
