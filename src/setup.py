from setuptools import setup

setup(
    name="mapping_tool",
    version="0.1",
    py_modules=["main"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        mapping_tool=main:cli
    """,
)
