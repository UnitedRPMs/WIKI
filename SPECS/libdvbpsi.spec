#AutoReqProv: no
#global pre _pre3

Summary: 	Library for MPEG TS and DVB PSI tables decoding and generation
Name: 		libdvbpsi
Version: 	1.3.0
Release: 	1%{?pre}%{?dist}
License: 	LGPLv2+
Group: 		System Environment/Libraries
URL: 		http://www.videolan.org/developers/libdvbpsi.html
Source0: 	http://download.videolan.org/pub/libdvbpsi/%{version}/%{name}-%{version}%{?pre}.tar.bz2
BuildRequires:	graphviz doxygen
Requires:	glibc >= 2.21
Requires:	rpm >= 4.6

%package devel
Summary: 	Development package for %{name}
Group: 		Development/Libraries
Requires: 	%{name} = %{version}-%{release}


%description
libdvbpsi is a very simple and fully portable library designed for
MPEG TS and DVB PSI table decoding and generation.

%description devel
libdvbpsi is a very simple and fully portable library designed for
MPEG TS and DVB PSI table decoding and generation.
This package contains development files for %{name}


%prep
%setup -q -n %{name}-%{version}%{?pre}



%build
./configure --prefix=/usr --libdir=%{_libdir}
make %{?_smp_mflags}
make doc 


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/%{name}.so.*
%{_libdir}/libdvbpsi.a

%files devel
%doc doc/doxygen/html
%{_includedir}/dvbpsi/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libdvbpsi.pc


%changelog

* Tue Jul 14 2015 <davidjeremias82 AT gmail DOT com> 1.3.0-1
- Updated to 1.3.0

* Wed Apr 22 2015 <davidjeremias82 AT gmail DOT com> 1.2.0-2
- Disabled ReqPro macro for compatibility and testing purposes.

* Sat Nov 15 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Nov 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.2-1
- Update to 1.1.2

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.0-1
- Update to 1.0.0
- Clean-up spec file

* Sun Nov 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.0-0.2_pre3
- Update to _pre3 as tagged in git

* Thu Oct 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.0-0.1_pre2
- Update to 1.0.0_pre2

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 05 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.2.2-1
- Update to 0.2.2

* Tue May 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.2.0-1
- Update to 0.2.0
- Switch to LGPLv2+

* Sat Apr 24 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.1.7-1
- Update to 0.1.7

* Sat Oct 17 2009 kwizart < kwizart at gmail.com > - 0.1.6-6
- Rebuild

* Sun Apr  5 2009 kwizart < kwizart at gmail.com > - 0.1.6-5
- Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.1.6-4
- rebuild for new F11 features

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.1.6-3
- rebuild

* Tue Feb 26 2008 kwizart < kwizart at gmail.com > - 0.1.6-2
- Rebuild for gcc43

* Mon Oct 22 2007 kwizart < kwizart at gmail.com > - 0.1.6-1
- Update to 0.1.6

* Sun Oct 14 2007 kwizart < kwizart at gmail.com > - 0.1.5-3
- Rpmfusion Merge Review

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.1.5-2
- Drop Epoch completely

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Jul 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.5-0.lvn.1
- 0.1.5.
- Build with dependency tracking disabled.
- Miscellaneous specfile cleanups.

* Mon May 17 2004 Dams <anvil[AT]livna.org> - 0:0.1.3-0.lvn.4
- Added url in Source0

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.3
- Removed comment after scriptlets

* Mon Aug 18 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.2
- Moved some doc to devel package

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.1
- Added post/postun scriptlets
- Using RPM_OPT_FLAGS
- Updated to 0.1.3

* Sun Jun 29 2003 Dams <anvil[AT]livna.org> 
- Initial build.
