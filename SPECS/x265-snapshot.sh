#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
name=x265
package=x265
branch=1.9

pushd "$tmp"
git clone -b ${branch} --depth 1 https://github.com/videolan/${package}.git
cd ${package}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=${branch} 

cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}
