for f in *src.rpm; do  echo "Processing $f"; rpm2cpio $f | cpio -civ '*.patch'; done;
