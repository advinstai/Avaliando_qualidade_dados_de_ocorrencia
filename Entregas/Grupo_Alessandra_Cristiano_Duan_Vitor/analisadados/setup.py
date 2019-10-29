import setuptools


setuptools.setup(
    name="analisadados", 
    version="1.0.0",
    author="GrupoACDV",
    author_email="author@example.com",
    description="Analise dos datasets ICMBio",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # em caso de erro comentar
    install_requires=['numpy','pandas','opencage'],
    python_requires='>=3.6',
)