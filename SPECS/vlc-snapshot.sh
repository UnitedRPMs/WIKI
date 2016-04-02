#!/bin/bash


set -x

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
package=vlc
branch=master
name=vlc

pushd ${tmp}
git clone --depth 1 https://github.com/videolan/vlc.git
cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`cat configure.ac | grep 'AC_INIT' | awk -F 'vlc, ' '{print $2}' | awk -F '-git' '{print $1}'`
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}



