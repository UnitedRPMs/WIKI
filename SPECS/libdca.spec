Summary: DTS Coherent Acoustics decoder library
Name: libdca
Version: 0.0.5
Release: 9%{?dist}
URL: http://www.videolan.org/developers/libdca.html
Group: System Environment/Libraries
Source: http://download.videolan.org/pub/videolan/libdca/0.0.5/%{name}-%{version}.tar.bz2
License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libdca is a free library for decoding DTS Coherent Acoustics streams. It is
released under the terms of the GPL license. The DTS Coherent Acoustics
standard is used in a variety of applications, including DVD, DTS audio CD and
radio broadcasting.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Obsoletes: libdts-devel < 0.0.2-2
Provides: libdts-devel = 0.0.2-2
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for %{name}.

Install %{name}-devel if you wish to develop or compile
applications that use %{name}.

%package tools
Summary: Various tools for use with %{name}
Group: Applications/Multimedia

%description tools
Various tools that use %{name}.

%prep
%setup -q

%build

./configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --disable-static
  make

%install

make DESTDIR=$RPM_BUILD_ROOT install 
rm -f %{buildroot}/%{_libdir}/%{name}.la

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/%{name}.so.*
%{_libdir}/libdts.a

%files tools
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc TODO doc/%{name}.txt
%{_libdir}/pkgconfig/libdca.pc
%{_libdir}/pkgconfig/libdts.pc
%{_includedir}/d??.h
%{_libdir}/%{name}.so


%changelog

* Tue Jul 14 2015 <davidjeremias82 AT gmail DOT com> 0.0.5-9
- Upstream
- A clean spec

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.5-7
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 17 2009 kwizart < kwizart at gmail.com > - 0.0.5-5
- Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.5-4
- rebuild for new F11 features

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.5-3
- rebuild

* Fri Nov  2 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.0.5-2
- Merge freshrpms spec into livna spec for rpmfusion:
- Update to latest upstream releae 0.0.5 as used by freshrpms
- Set release to 2 to be higher as both livna and freshrpms latest release
- Drop x86_64 patch (not needed since we override OPT_CFLAGS anyways)
- Drop visibility patch, this should be done upstream
- Drop upstream integrated libtool patch
- No longer regenerate the autoxxx scripts as this is no longer needed
- Port strict aliasing patch to 0.0.5 release
- Add relative symlink creation patch from freshrpms
- Update license tag in accordance with new license tag guidelines

* Sat Nov 25 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-3
- added patches from gentoo (shared build, strict aliasing and visibility)

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-2
- renamed to libdca
- added Obsoletes/Provides
- simplified autotools call

* Mon Aug 07 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-1
- stop pretending we have a newer version

* Sat Apr 16 2005 Dominik Mierzejewski <rpm@greysector.net> 0.0.3-0.20040725.1
- adapted ArkLinux specfile
- x86_64 portability patch

* Sun Jul 25 2004 Bernhard Rosenkraenzer <bero@arklinux.org> 0.0.3-0.20040725.1ark
- Force -fPIC
- Update

* Wed Jul 07 2004 Bernhard Rosenkraenzer <bero@arklinux.org> 0.0.3-0.20040707.1ark
- initial RPM
