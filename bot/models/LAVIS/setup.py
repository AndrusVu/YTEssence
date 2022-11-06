from setuptools import setup, find_namespace_packages
import platform

DEPENDENCY_LINKS = []
if platform.system() == "Windows":
    DEPENDENCY_LINKS.append("https://download.pytorch.org/whl/torch_stable.html")


def fetch_requirements(filename):
    with open(filename) as f:
        return [ln.strip() for ln in f.read().split("\n")]


setup(
    name="lavis",
    version="0.1.1",
    description="LAVIS - A Library for Language-Vision Intelligence",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="Vision-Language, Deep Learning, Library",
    packages=find_namespace_packages(include="lavis.*"),
    install_requires=fetch_requirements("requirements-wip.txt"),
    python_requires=">=3.8.0",
    include_package_data=True,
    dependency_links=DEPENDENCY_LINKS,
    zip_safe=False,
)