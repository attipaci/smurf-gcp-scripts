#!/bin/bash
#
# Undo all command symlinks in gcp/masd/keck/scripts
#
# Author: Attila Kovacs <attila.kovacs@cfa.harvard.edu>
# Version: 17 October 2018
#

MCESCRIPTS="$HOME/gcp/masd/keck/scripts"

for file in $MCESCRIPTS/* ; do 
  if [ -L $file ]; then
    rm -f $file
  fi
done

echo "Removed all MASD command links..."

