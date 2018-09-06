from setuptools import setup

setup(
    name="screenshot_detector",
    version="0.1",
    author="Duc Nguyen",
    author_email="ducnt4@vng.com.vn",
    description="detect screenshot base on edge detection",
    license="BSD",
    url="https://github.com/dukn/louvain_local",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
    ],

    packages=['screenshot_detector'],
    install_requires=[
        "scipy",
        "pillow",
        "pandas",
    ],
)
