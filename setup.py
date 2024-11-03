from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Custom Trained Gemini Flash',
    version='0.0.1',
    author='Shubham Gupta',
    author_email='data.guptashubh@gmail.com',
    description='Custom Trained Gemini Flash (CTGF) helps in Chat with your custom data',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
