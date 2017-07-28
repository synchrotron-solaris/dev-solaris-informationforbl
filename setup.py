from setuptools import find_packages, setup
from information_for_beamlines_ds.version import __version__, licence
from information_for_beamlines_ds import __doc__, __author__, __author_email__

setup(
    name="tangods-information_for_beamlines",
    author=__author__,
    author_email=__author_email__,
    version=__version__,
    license=licence,
    description="Tango InformationForBeamlines device server based on the facadedevice library",
    long_description=__doc__,
    url="https://github.com/synchrotron-solaris/dev-solaris-informationforbl.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["setuptools", "facadedevice", "pytango"],
    entry_points={
        "console_scripts": ["InformationForBeamlines = "
                            "information_for_beamlines_ds.information_for_beamlines.InformationForBeamlines:run"]}
)
