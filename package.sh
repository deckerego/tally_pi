#!/bin/sh

VERSION='0.1.0'
ARCHP='armhf'

# Package
cd ..
echo "Compressing file..."
tar Jcf "tallypi_$VERSION.orig.tar.xz" tally_pi/

cd tally_pi
dpkg-buildpackage -rfakeroot -uc -us

# Cleanup
echo "Cleaning up artifacts..."
rm "../tallypi_$VERSION-1_$ARCHP.buildinfo"
rm "../tallypi_$VERSION-1_$ARCHP.changes"
rm "../tallypi_$VERSION-1.debian.tar.xz"
rm "../tallypi_$VERSION-1.dsc"
rm "../tallypi_$VERSION.orig.tar.xz"
