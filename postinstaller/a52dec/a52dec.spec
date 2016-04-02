Summary: 	A free ATSC A/52 stream decoder
Name: 		a52dec
Version: 	0.7.4
Release: 	19%{?dist}
License: 	GPLv2
Group: 		System Environment/Libraries
URL: 		http://liba52.sourceforge.net/
Source0: 	http://liba52.sourceforge.net/files/%{name}-%{version}.tar.gz
Patch0:		a52dec-configure-optflags.patch
Patch1:		a52dec-0.7.4-rpath64.patch
Patch2:         liba52-silence.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	%{__perl}

%package devel
Summary:	Development files needed for a52dec
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

#---------------------------------------------------------------------

%description
liba52 is a free library for decoding ATSC A/52 streams. The A/52
standard is used in a variety of applications, including digital
television and DVD. It is also known as AC-3. The package also
includes a52dec, a small test program for liba52.

%description devel
liba52 is a free library for decoding ATSC A/52 streams. The A/52
standard is used in a variety of applications, including digital
television and DVD. It is also known as AC-3.
This package contains development files for a52dec.

#---------------------------------------------------------------------

%prep
%setup -q
%patch0
%patch1 -p1
%patch2 -p1
%{__perl} -pi -e 's/-prefer-non-pic\b/-prefer-pic/' \
  configure liba52/configure.incl

#---------------------------------------------------------------------

%build
%configure --enable-shared --disable-static
make %{?_smp_mflags}

#---------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

#---------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%exclude %{_libdir}/liba52.la
%doc AUTHORS COPYING ChangeLog HISTORY NEWS TODO
%{_libdir}/liba52.so.*
%{_bindir}/a52dec
%{_bindir}/extract_a52
%{_mandir}/man1/a52dec.1*
%{_mandir}/man1/extract_a52.1*

%files devel
%defattr(-,root,root,-)
%doc doc/liba52.txt
%{_includedir}/a52dec
%{_libdir}/liba52.so

#---------------------------------------------------------------------

%changelog
* Sat Aug 30 2014 Sérgio Basto <sergio@serjux.com> - 0.7.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-18
- Add silence patch as we don't built with DJBFFT enabled

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-17
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.4-15
- rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.4-14
- rebuild for new F11 features

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.4-12
- integrate a fix from livna that got lost

* Thu Jul 24 2008 David Juran <david@juran.se> - 0.7.4-12
- Bump Release for RpmFusion

* Sun Nov 11 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 0.7.4-11.1
- Really drop djbfft

* Mon Oct  1 2007 David Juran <david@juran.se> - 0.7.4-11
- Fix Licence tag to be GPLv2
- Drop %makeinstall macro
- Drop static archive
- Drop djbfft

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.7.4-10
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0.7.4-9
- Drop epoch in devel dep, too

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Feb 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.4-0.lvn.8
- Avoid standard rpaths on lib64 archs.

* Tue Jul 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.4-0.lvn.7
- Prefer PIC.
- (Build)Require djbfft-devel.
- Include more docs.

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.6
- Removed comment after scriptlets
- buildroot -> RPM_BUILD_ROOT

* Mon Apr 14 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.5
- devel package require djbfft (not djbfft-devel)

* Sun Apr 13 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.4
- Enabled support for djbfft

* Sun Apr 13 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.3
- Added post and postun scriplet
- moved man pages from devel to main package

* Sun Apr 13 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.2
- make configure honor optflags
- devel package
- shared library added

* Thu Apr 10 2003 Dams <anvil[AT]livna.org> 
- Initial build.
