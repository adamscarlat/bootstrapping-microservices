import setuptools

setuptools.setup(
  name = "flixtube_common",
  version="0.0.8",
  author="me",
  description="Common code for the FlixTube application",
  install_requires=[
    'motor==3.4.0',
    'aio-pika==9.4.1'
  ],
  package_dir = {"": "src"},
  packages = setuptools.find_packages(where="src"),
  python_requires = ">=3.6"
)