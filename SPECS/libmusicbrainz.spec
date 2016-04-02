# globals for libmusicbrainz5-5.1.0-20160223-2adc507.tar.xz
%global gitdate 20160223
%global gitversion 2adc507
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

Summary: Library for accessing MusicBrainz servers
Name: libmusicbrainz5
Version: 5.1.0
Release: 1%{?gver}%{dist}

License: LGPLv2+
URL: http://www.musicbrainz.org/
Source:	%{name}-%{version}-%{snapshot}.tar.xz
Source1: %{name}-snapshot.sh

BuildRequires: cmake
%if 0%{?_with_check}
BuildRequires: cppunit-devel
%endif
#BuildRequires: doxygen
BuildRequires: libdiscid-devel
BuildRequires: neon-devel
BuildRequires: pkgconfig
BuildRequires: libxml2-devel
Requires: libxml2

%description
The MusicBrainz client library allows applications to make metadata
lookup to a MusicBrainz server, generate signatures from WAV data and
create CD Index Disk ids from audio CD roms.

%package devel
Summary: Headers for developing programs that will use %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains the headers that programmers will need to develop
applications which will use %{name}. 


%prep
%setup -n libmusicbrainz


%build
%cmake .
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -fv docs/installdox

%check
ctest -V %{?_smp_mflags}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS.txt COPYING.txt NEWS.txt 
%{_libdir}/libmusicbrainz5.so.*

%files devel
%{_includedir}/musicbrainz5/
%{_libdir}/libmusicbrainz5.so
%{_libdir}/pkgconfig/libmusicbrainz5.pc


%changelog

* Mon Feb 22 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 5.1.0-1
- Initial build
