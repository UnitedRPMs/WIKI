%global	 realname  freerdp	

Name:           freerdp1
Version:        1.0.2
Release:        2%{?dist}
Summary:        Remote Desktop Protocol client

Group:          Applications/Communications
License:        ASL 2.0
URL:            http://www.freerdp.com/
Source0:        http://pub.freerdp.com/releases/freerdp-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  xmlto
BuildRequires:  openssl-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXv-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  cups-devel
BuildRequires:  pcsc-lite-devel
BuildRequires:  desktop-file-utils

Provides:       xfreerdp = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-plugins%{?_isa} = %{version}-%{release}

%description
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP
project.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.


%package        libs
Summary:        Core libraries implementing the RDP protocol
Group:          Applications/Communications
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.


%package        plugins
Summary:        Plugins for handling the standard RDP channels
Group:          Applications/Communications
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description    plugins
A set of plugins to the channel manager implementing the standard virtual
channels extending RDP core functionality. For instance, sounds, clipboard
sync, disk/printer redirection, etc.


%package        devel
Summary:        Development files for %{realname}
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{realname}-devel package contains libraries and header files for
developing applications that use %{realname}-libs.


%prep

%setup -n freerdp-%{version}


cat << EOF > xfreerdp1.desktop 
[Desktop Entry]
Type=Application
Name=X FreeRDP 1
NoDisplay=true
Comment=Connect to RDP server and display remote desktop
Icon=%{realname}
Exec=/usr/bin/freerdp1/xfreerdp
Terminal=false
Categories=Network;RemoteAccess;
EOF


%build

export CFLAGS="-fPIC %{optflags}"

cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/%{realname}-%{version} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_SKIP_INSTALL_RPATH=ON \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}/ \
	-DCMAKE_INSTALL_BINDIR=%{_bindir}/freerdp1 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
        -DWITH_CUPS=ON \
        -DWITH_PCSC=ON \
        -DWITH_PULSEAUDIO=ON \
        -DWITH_X11=ON \
        -DWITH_XCURSOR=ON \
        -DWITH_XEXT=ON \
        -DWITH_XINERAMA=ON \
        -DWITH_XKBFILE=ON \
        -DWITH_XV=ON \
        -DWITH_ALSA=OFF \
        -DWITH_CUNIT=OFF \
        -DWITH_DIRECTFB=OFF \
        -DWITH_FFMPEG=OFF \
        -DWITH_SSE2=OFF \
        .

make %{?_smp_mflags} all


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=%{buildroot} INSTALL='install -p'

# No need for keymap files when using xkbfile
rm -rf %{buildroot}/opt/%{realname}-%{version}/share/freerdp/keymaps/

desktop-file-install --dir=%{buildroot}/%{_datadir}/applications xfreerdp1.desktop
install -p -m 644 -D resources/FreeRDP_Icon_256px.png %{buildroot}/%{_datadir}/icons/hicolor/256x256/apps/%{realname}.png

install -dm 755 %{buildroot}/%{_libdir}/pkgconfig/
ln -sf /opt/%{realname}-%{version}/%{_lib}/pkgconfig/%{realname}.pc %{buildroot}/%{_libdir}/pkgconfig/%{realname}-1.pc

%clean
rm -rf %{buildroot}


%post
# This is no gtk application, but try to integrate nicely with GNOME if it is available
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}/xfreerdp
/opt/%{realname}-%{version}/share/man/man1/xfreerdp.1
%{_datadir}/applications/xfreerdp1.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{realname}.png

%files libs
%defattr(-,root,root,-)
%doc LICENSE README ChangeLog
/opt/%{realname}-%{version}/%{_lib}/lib%{realname}-*.so.*


%files plugins
%defattr(-,root,root,-)
/opt/%{realname}-%{version}/%{_lib}/%{realname}/audin_pulse.so  
/opt/%{realname}-%{version}/%{_lib}/%{realname}/drdynvc.so   
/opt/%{realname}-%{version}/%{_lib}/%{realname}/rdpdbg.so        
/opt/%{realname}-%{version}/%{_lib}/%{realname}/scard.so
/opt/%{realname}-%{version}/%{_lib}/%{realname}/audin.so        
/opt/%{realname}-%{version}/%{_lib}/%{realname}/parallel.so  
/opt/%{realname}-%{version}/%{_lib}/%{realname}/rdpdr.so         
/opt/%{realname}-%{version}/%{_lib}/%{realname}/serial.so
/opt/%{realname}-%{version}/%{_lib}/%{realname}/cliprdr.so      
/opt/%{realname}-%{version}/%{_lib}/%{realname}/printer.so   
/opt/%{realname}-%{version}/%{_lib}/%{realname}/rdpsnd_pulse.so  
/opt/%{realname}-%{version}/%{_lib}/%{realname}/tsmf_pulse.so
/opt/%{realname}-%{version}/%{_lib}/%{realname}/disk.so         
/opt/%{realname}-%{version}/%{_lib}/%{realname}/rail.so      
/opt/%{realname}-%{version}/%{_lib}/%{realname}/rdpsnd.so        
/opt/%{realname}-%{version}/%{_lib}/%{realname}/tsmf.so

%files devel
%defattr(-,root,root,-)
/opt/%{realname}-%{version}/include/%{realname}/
/opt/%{realname}-%{version}/%{_lib}/lib%{realname}-*.so
/opt/%{realname}-%{version}/%{_lib}/pkgconfig/%{realname}.pc
%{_libdir}/pkgconfig/%{realname}-1.pc


%changelog

* Mon Mar 23 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.0.2-2
- Repaired conflict path, with the current freerdp-devel

* Mon Mar 23 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.0.2-1
- Initial build rpm for legacy support freerdp v.1
