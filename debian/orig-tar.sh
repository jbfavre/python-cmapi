#!/bin/sh -e

# $1 = --upstream-version
# $2 = version
# $3 = file_name
echo $1
echo $2
echo $3
exit 0
TAR=../python-cm-api-$2.orig.tar.gz
DIR=../python-cm-api-$2.orig

# clean up the upstream tarball
git clone https://github.com/cloudera/cm_api.git $DIR
GZIP="--best --no-name" tar -c -z -f $TAR $DIR/python
rm -rf $DIR
rm ../python-cm-api-$2

# move to directory 'tarballs'
if [ -r .svn/deb-layout ]; then
  . .svn/deb-layout
  mv $TAR $origDir
  echo "moved $TAR to $origDir"
fi
