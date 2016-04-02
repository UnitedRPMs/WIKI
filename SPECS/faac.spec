Name:           faac
Version:        1.28
Release:        7%{?dist}
Summary:        Encoder and encoding library for MPEG2/4 AAC

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://www.audiocoding.com/
Source0:        http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
Patch0:         %{name}-libmp4v2.patch

BuildRequires:  libtool
BuildRequires:  libmp4v2-devel



%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

%package devel
Summary:        Development libraries of the FAAC AAC encoder
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .mp4v2
#fix permissions
find . -type f \( -name \*.h -or -name \*.c \) -exec chmod 644 {} \;
chmod 644 AUTHORS COPYING ChangeLog NEWS README TODO docs/*

#fix encoding
/usr/bin/iconv -f iso8859-1 -t utf-8 AUTHORS > AUTHORS.conv && touch -r AUTHORS AUTHORS.conv && /bin/mv -f AUTHORS.conv AUTHORS

# Autotools
autoreconf -vif


%build
%configure --disable-static
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%doc AUTHORS COPYING ChangeLog NEWS README TODO docs/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/%{name}*

%files devel
%exclude  %{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Sat Dec  6 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.28-7
- Fix build with libmp4v2-devel - rfbz#3188
- Clean-up spec file

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.28-5
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 25 2009 kwizart < kwizart at gmail.com > - 1.28-2
- Install with -p
- Moved in nonfree

* Tue Apr 07 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.28-1.1
- rebuild

* Thu Mar 12 2009 Dominik Mierzejewski <rpm [AT] greysector [DOT] net> - 1.28-1
- update to 1.28
- drop redundant BRs
- fix Source URL and use bz2 tarball
- fix rpath
- include manpage

* Sun Dec 14 2008 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.26-1
- ship AUTHORS NEWS docs/*
- integrated changes from Julian Sikorski <belegdol[at]gmail[dot]com>
-- Updated to 1.26
-- Dropped dos2unix BR, not needed anymore
-- Made Source0 use macros
-- Fixed License tag
-- Fixed file permissions
-- Converted ChangeLog to utf-8

* Tue Nov 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.25-7
- chmod 644 all docs (fixes #115)

* Thu Jul 24 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.25-6
- rebuild

* Tue Jul 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.25-5
- rebuild for RPM Fusion

* Sat Sep 17 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.25-4
- update license tag

* Sat Sep 17 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.25-3
- incorporate some minor adjustments from the freshrpms pacakge

* Sun Dec 17 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.25-2
- BR dos2unix

* Sun Dec 17 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.25-1
- Update to 1.25
- appy patch from to enable build against libmp4v2 from #1317
  (thx to noa)

* Sat Sep 30 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.24-6
- rebuild for new libmp4v2-devel

* Sun May 28 2006 Noa Resare <noa@resare.com> 1.24-5
- libmp4v2 is now a separate package, updated BR
- shortened summary string

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.24-4
- Drop Epoch completely

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Oct 25 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.24-0.lvn.3
- BR automake autoconf (how could I have been that stupid and missed those? 
  don't answer please)

* Mon Oct 25 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.24-0.lvn.2
- BR libtool

* Fri Oct 22 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.24-0.lvn.1
- Initial RPM release. 
