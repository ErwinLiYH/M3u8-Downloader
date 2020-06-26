import setuptools

with open('README.md','r') as a:
    long_description = a.read()

setuptools.setup(
    name = 'mder',
    version = '1.0.1',  
    author = 'walkureHHH',
    author_email = '1779599839@qq.com',
    description = 'A multithreading m3u8 download module for python, and the number of threads can decide by yourself; Convert .m3u8 file to .mp4 file; Supporting redownload.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/walkureHHH/M3u8_Downloader',
    packages = ['mder'],
    install_requires = ['tqdm','requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",]
)
