Name: libcdio
Version: 0.93
Release: 2%{?dist}
Summary: CD-ROM input and control library
Group: System Environment/Libraries
License: GPLv3+
URL: http://www.gnu.org/software/libcdio/
Source0: http://ftp.gnu.org/gnu/libcdio/libcdio-0.93.tar.gz
Source1: http://ftp.gnu.org/gnu/libcdio/libcdio-0.93.tar.gz.sig
Source2: libcdio-no_date_footer.hml
Source3: cdio_config.h
# https://savannah.gnu.org/bugs/index.php?43995
Patch0: libcdio-0.93-udf-bigendian.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig doxygen
BuildRequires: ncurses-devel
BuildRequires: help2man
Requires(post): /sbin/ldconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: gettext-devel
BuildRequires: chrpath


%description
This library provides an interface for CD-ROM access. It can be used
by applications that need OS- and device-independent access to CD-ROM
devices.

%package devel
Summary: Header files and libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.


%prep
%setup -q
%patch0 -p1 -b .udf-bigendian

iconv -f ISO88591 -t utf-8 -o THANKS.utf8 THANKS && mv THANKS.utf8 THANKS

%build
%configure \
	--disable-vcd-info \
	--disable-dependency-tracking \
	--disable-cddb \
	--disable-static \
	--disable-rpath
make %{?_smp_mflags}

# another multilib fix; remove the architecture information from version.h
sed -i -e "s,%{version}.*$,%{version}\\\",g" include/cdio/version.h

cd doc/doxygen
sed -i -e "s,HTML_FOOTER.*$,HTML_FOOTER = libcdio-no_date_footer.hml,g; \
		s,EXCLUDE .*$,EXCLUDE = ../../include/cdio/cdio_config.h,g;" Doxyfile
cp %{SOURCE2} .
./run_doxygen

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# multilib header hack; taken from postgresql.spec
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x | sparc | sparc64 )
		mv $RPM_BUILD_ROOT%{_includedir}/cdio/cdio_config.h $RPM_BUILD_ROOT%{_includedir}/cdio/cdio_config_`uname -i`.h
		install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_includedir}/cdio
		;;
	*)
		;;
esac

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rm -rf examples
mkdir -p examples/C++
cp -a example/{*.c,README} examples
cp -a example/C++/{*.cpp,README} examples/C++

# fix timestamps of generated man-pages
for i in cd-info iso-read iso-info cd-read cd-drive; do 
	# remove build architecture information from man pages
	sed -i -e 's, version.*linux-gnu,,g' $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
	# remove libtool leftover from man pages
	sed -i -e 's,lt-,,g;s,LT-,,g' $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
	# fix timestamps to be the same in all packages
	touch -r src/$i.help2man $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
done

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so.*

%check
# disable test using local CDROM
%{__sed} -i -e "s,testiso9660\$(EXEEXT),,g" \
	    -e "s,testisocd\$(EXEEXT),,g" \
	    -e "s,check_paranoia.sh check_opts.sh, check_opts.sh,g" \
	    test/Makefile
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/%{name}.info \
		%{_infodir}/dir 2>/dev/null || :
fi

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README README.libcdio THANKS TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_infodir}/*
%{_mandir}/man1/*


%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html examples
%{_includedir}/cdio
%{_includedir}/cdio++
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Jan 13 2015 Dan Horák <dan[at]danny.cz> - 0.93-2
- add big endian fix for udf

* Fri Oct 31 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 0.93-1
- rebase to 0.93

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 Adrian Reber <adrian@lisas.de> - 0.92-1
- updated to 0.92

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Adrian Reber <adrian@lisas.de> - 0.90-1
- updated to 0.90

* Tue Jul 24 2012 Adrian Reber <adrian@lisas.de> - 0.83-5
- fixed #477288 (libcdio-devel multilib conflict) again

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Adrian Reber <adrian@lisas.de> - 0.83-3
- fixed #804484 (/usr/bin/cd-info was killed by signal 11)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 13 2011 Adrian Reber <adrian@lisas.de> - 0.83-1
- updated to 0.83

* Mon May 30 2011 Honza Horak <hhorak@redhat.com> - 0.82-5
- applied patch to fix issues found by static analyses

* Thu May 19 2011 Honza Horak <hhorak@redhat.com> - 0.82-4
- fixed #705673 buffer overflow and other unprotected sprintf calls

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 28 2010 Adrian Reber <adrian@lisas.de> - 0.82-2
- disabled building of static libraries (#556064)
- removed "Requires: pkgconfig" (rpm adds it automatically)

* Wed Jan 20 2010 Roman Rakus rrakus@redhat.com 0.82-1
- Update to 0.82
- removed rpath
- converted THANKS to utf8 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 07 2008 Adrian Reber <adrian@lisas.de> - 0.81-1
- updated to 0.81
- license changed to GPLv3+
- fixed #477288 (libcdio-devel multilib conflict)
- applied patch to fix endless loop in mock

* Tue Oct 07 2008 Adrian Reber <adrian@lisas.de> - 0.80-5
- fixed #462125 (Multilib conflict) - really, really, really
  (also remove architecture information from man pages)

* Thu Oct 02 2008 Adrian Reber <adrian@lisas.de> - 0.80-4
- fixed #462125 (Multilib conflict) - this time for real

* Fri Sep 12 2008 Adrian Reber <adrian@lisas.de> - 0.80-3
- fixed #462125 (Multilib conflict)

* Wed Jun  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.80-2
- added patch enabling libcdio_paranoia.pc

* Thu May 29 2008 Adrian Reber <adrian@lisas.de> - 0.80-1
- updated to 0.80
- removed upstreamed patches
- last GPLv2+ release

* Thu Feb 14 2008 Adrian Reber <adrian@lisas.de> - 0.79-3
- added patch to compile with gcc43

* Fri Jan 04 2008 Adrian Reber <adrian@lisas.de> - 0.79-2
- fixed security fix (was off by two)

* Wed Jan 02 2008 Adrian Reber <adrian@lisas.de> - 0.79-1
- updated to 0.79
- fixes #427197 (Long Joliet file name overflows cdio's buffer)
- fixes #341981 (multiarch conflicts in libcdio)

* Fri Aug 24 2007 Adrian Reber <adrian@lisas.de> - 0.78.2-3
- rebuilt

* Mon Jul 23 2007 Adrian Reber <adrian@lisas.de> - 0.78.2-2
- updated to 0.78.2 (#221359) (this time for real)

* Thu Jan 04 2007 Adrian Reber <adrian@lisas.de> - 0.78.2-1
- updated to 0.78.2 (#221359)

* Thu Oct 05 2006 Adrian Reber <adrian@lisas.de> - 0.77-3
- disabled iso9660 test case (fails for some reason with date problems)
  this seems to be a known problem according to the ChangeLog

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.77-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Adrian Reber <adrian@lisas.de> - 0.77-1
- Updated to 0.77

* Mon Sep 18 2006 Adrian Reber <adrian@lisas.de> - 0.76-3
- Rebuilt

* Mon Sep 26 2005 Adrian Reber <adrian@lisas.de> - 0.76-2
- Rebuilt

* Mon Sep 26 2005 Adrian Reber <adrian@lisas.de> - 0.76-1
- Updated to 0.76.
- Included doxygen generated documentation into -devel
- Included examples into -devel

* Mon Aug 01 2005 Adrian Reber <adrian@lisas.de> - 0.75-4
- disable test accessing local CDROM drive (#164266)

* Wed Jul 27 2005 Adrian Reber <adrian@lisas.de> - 0.75-3
- Rebuilt without libcddb dependency (#164270)

* Tue Jul 26 2005 Adrian Reber <adrian@lisas.de> - 0.75-2
- Rebuilt

* Thu Jul 14 2005 Adrian Reber <adrian@lisas.de> - 0.75-1
- Updated to 0.75.

* Fri Jun 03 2005 Adrian Reber <adrian@lisas.de> - 0.74-2
- Updated to 0.74.

* Sun Apr 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.73-2
- BuildRequire ncurses-devel (for cdda-player and cd-paranoia).
- Run test suite during build.
- Install Japanese man pages.

* Sun Apr 24 2005 Adrian Reber <adrian@lisas.de> - 0.73-1
- Updated to 0.73.

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.70-2
- Fix FC4 build (#151468).
- Build with dependency tracking disabled.

* Sun Sep  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.70-0.fdr.1
- Updated to 0.70.

* Sat Jul 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.69-0.fdr.1
- Updated to 0.69.
- Removed broken iso-read.
- Split Requires(pre,post).
- Added BuildReq pkgconfig.

* Mon Mar 29 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.68-0.fdr.1
- Initial RPM release.

