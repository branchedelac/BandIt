from setuptools import find_packages
from setuptools import setup

with open("requirements_prod.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='bandit',
      version="1.0.0",
      description="BandIt API",
      license="MIT",
      author="BandIt Team",
      author_email="branchedelac@gmail.com",
      url="https://github.com/MarkBerkovics/bandit",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
