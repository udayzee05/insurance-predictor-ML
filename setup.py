import os
from setuptools import setup,find_packages
from typing import List

REMOVE_PACKAGES = "-e ."

def get_requirements()->List[str]:
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
        requirenment_list = f.read().splitlines()
        if REMOVE_PACKAGES in requirenment_list:
            requirenment_list.remove(REMOVE_PACKAGES)
        return requirenment_list
    

setup(name='Insurance',
      version='1.0',
      description='End to end Insurance prediction',
      author='Uday Zope ',
      author_email='udayzee05@gmail.com',
      packages=find_packages(),
      install_requires=get_requirements(),
     )