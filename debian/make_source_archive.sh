#!/bin/bash

MICMAC_REPOSITORY=`basename $PWD`
#get local revision number
REV_NUMBER=`hg id -n`
OUT_MICMAC_DIR=micmac
ARCHIVE_NAME=micmac_1.0+hg$REV_NUMBER.orig
if [ -f $ARCHIVE_NAME.tar.gz ]
then
	echo $ARCHIVE_NAME.tar.gz already exists
	exit 1
fi
if [ -d $OUT_MICMAC_DIR ]
then
	echo $OUT_MICMAC_DIR already exists
	exit 1
fi
mkdir $OUT_MICMAC_DIR
cp -R CodeGenere $OUT_MICMAC_DIR
cp -R CodeExterne $OUT_MICMAC_DIR
cp -R data $OUT_MICMAC_DIR
cp -R include $OUT_MICMAC_DIR
cp -R src $OUT_MICMAC_DIR
cp CMakeLists.txt $OUT_MICMAC_DIR
cp Makefile-XML2CPP $OUT_MICMAC_DIR
cp precompiled_headers.cmake $OUT_MICMAC_DIR
cp README $OUT_MICMAC_DIR
cp LISEZMOI $OUT_MICMAC_DIR

rm -fr $OUT_MICMAC_DIR/include/StdAfx.h.gch
rm -fr $OUT_MICMAC_DIR/data/Tabul/.svn
rm -fr $OUT_MICMAC_DIR/src/interface

# remove hg
rm -rf $OUT_MICMAC_DIR/.hg .hgignore

# tmp files
find $OUT_MICMAC_DIR/ -name *~ -exec rm {} \;

# Sanitize perms
# TODO: I am not so sure about that...
find $OUT_MICMAC_DIR/ -type f -exec chmod -R 644 {} \;

###########################
# TODO: Sanitize encoding #
###########################

tar czf $ARCHIVE_NAME.tar.gz $OUT_MICMAC_DIR
rm -fr $OUT_MICMAC_DIR
