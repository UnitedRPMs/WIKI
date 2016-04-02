#!/bin/bash

tag_name=release-5.1.0

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
package=libmusicbrainz
branch=master
name=libmusicbrainz5

pushd ${tmp}
git clone -b ${tag_name} --depth 1 https://github.com/metabrainz/libmusicbrainz.git
cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`git describe --tags | awk -F 'release-' '{print $2}'`
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}



