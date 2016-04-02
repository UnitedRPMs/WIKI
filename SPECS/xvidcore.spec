%global debug_package %{nil}
%define soname  4
 
Name:           xvidcore
Version:        1.3.4
Release:        1%{?dist}
Summary:        MPEG-4 Simple and Advanced Simple Profile codec

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.xvid.org/
Source:		http://downloads.xvid.org/downloads/xvidcore-%{version}.tar.bz2
Source1:        baselibs.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%ifarch %{ix86} x86_64
BuildRequires:  nasm >= 2.0
%endif

Provides:       xvid = %{version}
Obsoletes:      xvid < %{version}

%description
The Xvid video codec implements MPEG-4 Simple Profile and Advanced Simple
Profile standards. It permits compressing and decompressing digital video
in order to reduce the required bandwidth of video data for transmission
over computer networks or efficient storage on CDs or DVDs. Due to its
unrivalled quality Xvid has gained great popularity and is used in many
other GPLed applications, like e.g. Transcode, MEncoder, MPlayer, Xine and
many more.

%package        devel
Summary:        Development files for the Xvid video codec
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files, static library and API
documentation for the Xvid video codec.


%prep
%setup -q -n %{name}
sed -i '1i%%ifidn __OUTPUT_FORMAT__,elf\nSECTION .note.GNU-stack noalloc progbits noexec nowrite\n%%endif' src/*/*_asm/*.asm

%build

pushd build/generic
%configure
make %{?_smp_mflags}
popd


%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
mkdir %{buildroot}
install -d "%{buildroot}%{_libdir}"
install -d "%{buildroot}%{_includedir}"

pushd 'build/generic/=build'
install *.so* "%{buildroot}%{_libdir}/"
popd #'build/generic/=build'

pushd src
install xvid.h "%{buildroot}%{_includedir}/"
popd #src

pushd "%{buildroot}%{_libdir}"
ln -s libxvidcore.so.%{soname}.* libxvidcore.so.%{soname}
ln -s libxvidcore.so.%{soname} libxvidcore.so
popd #libdir

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README AUTHORS ChangeLog
%{_libdir}/libxvidcore.so.*

%files devel
%defattr(-,root,root,-)
%doc CodingStyle TODO examples/
%{_includedir}/xvid.h
%{_libdir}/libxvidcore.so


%changelog

* Fri Feb 19 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.3.4-1
- Updated to 1.3.4

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Mar 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-5
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-2
- Update to 1.3.2

* Mon Jan 10 2011 Dominik Mierzejewski <rpm at greysector.net> - 1.3.0-0.1.rc1
- 1.3.0-rc1
- drop upstreamed noexec stack patch

* Sat Dec 11 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.2.2-1
- 1.2.2
- rebase noexec-stack patch

* Mon Sep 21 2009 Hans de Goede <j.w.r.degoede@hhs.nl> - 1.2.1-3
- Do not require an executable stack on x86_64 (rf743, rf733)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.2.1-2
- rebuild for new F11 features

* Sat Dec 20 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.2.1-1
- 1.2.1
- drop upstreamed compilation fix

* Wed Dec 03 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.2.0-1
- 1.2.0
- drop upstreamed noexec stack patch
- BR recent nasm instead of yasm
- licence seems to be just GPLv2+
- move TODO from main to -devel doc
- update summary and description
- small spec file fixes

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.1.3-4
- rebuild

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.3-3
- Merge freshrpms spec into livna spec for rpmfusion:
- Set release to 3 to be higher as both livna and freshrpms latest release
- Add -ffast-math to CFLAGS

* Sat Jun 30 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.1.3-1
- 1.1.3, security bugfix release, fixes CVE-2007-3329 (#1563)

* Sun Mar 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.1.2-2
- fix SElinux noexec stack issue (patch by Hans de Goede)

* Sat Nov 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.2-1
- 1.1.2.
- Convert docs to UTF-8.
- Use make install DESTDIR=... instead of %%makeinstall.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.1.0-4
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.0-3
- Use yasm to build, enable asm code on x86_64.
- Drop no longer needed Obsoletes.
- Specfile cleanups.

* Sat May 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.0-2
- Fix library permissions and symlink.
- Don't ship static library.
- Avoid -devel dependency on perl.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Jan 18 2006 Adrian Reber <adrian@lisas.de> - 1.1.0-0.lvn.1
- Updated to 1.10
- Droped now unnecessary patch
- Droped Epoch

* Sun Feb 20 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.3-0.lvn.1
- 1.0.3.

* Wed Sep 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.2-0.lvn.1
- Update to 1.0.2.

* Tue Jun  8 2004 Dams <anvil[AT]livna.org> 0:1.0.1-0.lvn.1
- Updated to 1.0.1

* Mon May 17 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.1
- Updated to 1.0.0.
- Patch to show build output.

* Mon May  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.0.2.rc4
- Updated to 1.0.0-rc4.

* Mon Mar 29 2004 Dams <anvil[AT]livna.org> 0:1.0.0-0.lvn.0.2.rc3
- Updated to rc3

* Sat Jan 10 2004 Dams <anvil[AT]livna.org> 0:1.0.0-0.lvn.0.1.beta3
- Updated to 1.0.0-beta3
- Small spec file cleanup

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.1.0.94
- Removed comment after scriptlets

* Fri Aug 15 2003 Marius L. Johndal <mariuslj at ifi.uio.no> 0:0.9.2-0.fdr.1
- Updated to 0.9.2.
- Updated according to current SPEC template.
- Changed to properly versioned .so-files.

* Tue Apr  8 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.3
- Cleaned up the documentation.

* Fri Apr  4 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.2
- Added epoch and release number to requires.

* Wed Apr  2 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.1
- Updated to 0.9.1.

* Wed Apr  2 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.0-0.fdr.1
- Initial fedora RPM release.
- Changed -static back to -devel as that seems more logic.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.

* Wed Jan 29 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fixed the location of the .h files... doh!

* Sun Jan 12 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Remove the decore.h and encore2.h inks as divx4linux 5.01 will provide them.
- Rename -devel to -static as it seems more logic.

* Fri Dec 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
