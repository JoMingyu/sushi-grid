from setuptools import setup

setup(
    name="sushi-grid",
    description="CLI tool for make sushi samples grid automatically",
    version="0.0.1",
    url="https://github.com/JoMingyu/sushi-grid",
    license="MIT License",
    author="PlanB",
    author_email="mingyu.planb@gmail.com",
    maintainer="PlanB",
    maintainer_email="mingyu.planb@gmail.com",
    install_requires=["click"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["app"],
    entry_points={
        "console_scripts": [
            "grid = app.cli:handler",
        ],
    },
)
