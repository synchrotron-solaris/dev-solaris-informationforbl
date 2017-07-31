"""
DEVICE CLASS INFORMATION FOR BEAMLINES SOLARIS
==============================================

This package contains InformationForBeamlines device class
based on the facadedevice library. It stores communication
between Control Room and beamlines.
"""

from setuptools import find_packages

__all__ = ['information_for_beamlines_ds', 'version']
__doc__ = ""
__author__ = "Michal Piekarski"
__author_email__ = "michalpiekars@gmail.com"

package_name=find_packages()
package_import = __import__(package_name)
__doc__ += "%s: %s" % (package_name, package_import.__doc__)
__author__ += package_import.__author__ + ", "
__author_email__ += package_import.__author_email__ + ", "
