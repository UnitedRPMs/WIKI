Name:           libmpeg2
Version:        0.5.1
Release:        11%{?dist}
Summary:        MPEG-2 decoder libraries

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://libmpeg2.sourceforge.net/
Source0:        http://libmpeg2.sourceforge.net/files/libmpeg2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  SDL-devel
BuildRequires:  libXt-devel
BuildRequires:  libXv-devel


%description
libmpeg2 is a free library for decoding mpeg-2 and mpeg-1 video
streams. It is released under the terms of the GPL license.

%package -n     mpeg2dec
Summary:        MPEG-2 decoder program
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description -n mpeg2dec
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
# Introducted in F-10 Can be dropped in F-12
Provides:       mpeg2dec-devel = %{version}-%{release}
Obsoletes:      mpeg2dec-devel < %{version}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
iconv -f ISO-8859-1 -t UTF-8 AUTHORS > AUTHORS.tmp
touch -r AUTHORS AUTHORS.tmp 
cp -p -f AUTHORS.tmp AUTHORS
rm AUTHORS.tmp

#Disable ppc altivec case
sed -i -e 's/ppc-/noppc64-/' configure.ac configure
sed -i -e 's/powerpc-/nopowerpc64-/' configure.ac configure

%build
%configure --disable-static \
%ifarch %{ix86} ppc
  --disable-accel-detect \
%endif

# mpeg2dec have rpath
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} \
%ifarch %{ix86}
  OPT_CFLAGS="-fPIC -DPIC" \
%else
  OPT_CFLAGS="" \
%endif


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


#Fix datatype internal definitions
install -pm 0644 libmpeg2/mpeg2_internal.h \
  $RPM_BUILD_ROOT%{_includedir}/mpeg2dec/



%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_libdir}/*.so.*

%files -n mpeg2dec
%defattr(-,root,root,-)
%{_bindir}/corrupt_mpeg2
%{_bindir}/extract_mpeg2
%{_bindir}/mpeg2dec
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%doc CodingStyle doc/libmpeg2.txt doc/sample*.c
%{_includedir}/mpeg2dec/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmpeg2.pc
%{_libdir}/pkgconfig/libmpeg2convert.pc


%changelog
* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-10
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 17 2009 kwizart < kwizart at gmail.com > - 0.5.1-8
- Rebuild for F-12

* Wed Apr  8 2009 kwizart < kwizart at gmail.com > - 0.5.1-7
- New attempt

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.5.1-6
- rebuild for new F11 features

* Fri Mar 27 2009 kwizart < kwizart at gmail.com > - 0.5.1-5
- Rebuild
- Fix target_arch conditionals
- Provides internal definitions mpeg2_internal.h
- Disable ppc altivec optim (TODO improve asm optim later)
 
* Fri Oct  4 2008 kwizart < kwizart at gmail.com > - 0.5.1-3
- Fix CFLAGS on x86 producing selinux denials.

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.5.1-2
- rebuild for buildsys cflags issue

* Fri Jul 18 2008 kwizart < kwizart at gmail.com > - 0.5.1-1
- Update to 0.5.1

* Tue Jul 15 2008 kwizart < kwizart at gmail.com > - 0.5.0-1
- Initial package (based on mpeg2dec)

