%define name kismet


# numbering scheme 
# month + year + tiny
# i hope they will not release a real 3.1
# numbering : Year Month Number ( so feb 2004, first version is 040201 )
%define version 3.1.060413
%define release %mkrel 2

Summary: Kismet is an 802.11b/g network sniffer and network dissector
Name: %name
Version: %version
Release: %release
Group: Networking/Other
License: GPL
Url: http://www.kismetwireless.net
Source: http://www.kismetwireless.net/code/%{name}-2006-04-R1.tar.bz2
BuildRoot: %_tmppath/%{name}-%{version}-buildroot
Buildrequires: libncurses-devel 
Buildrequires: libpcap-devel
Buildrequires: ImageMagick-devel
Buildrequires: wget
Buildrequires: glib-devel
BuildRequires: flex 
Buildrequires: bison
Buildrequires: gpsd-devel gmp-devel expat-devel

%description
Kismet is an 802.11b/g network sniffer and network dissector. It is
capable of sniffing using most wireless cards, automatic network IP
block detection via UDP, ARP, and DHCP packets, Cisco equipment lists
via Cisco Discovery Protocol, weak cryptographic packet logging, and
Ethereal and tcpdump compatible packet dump files. It also includes
the ability to plot detected networks and estimated network ranges on
downloaded maps or user supplied image files.

%prep

%setup -q -n %{name}-2006-04-R1
perl -pi -e 's/-o \$\(INSTUSR\) -g \$\(INSTGRP\)//' Makefile.in
perl -pi -e 's/-o \$\(INSTUSR\) -g \$\(MANGRP\)//' Makefile.in
cat <<EOF > fix.h
#ifndef __FIX_H__
#define __FIX_H__
#define u32 __u32
#define u64 __u64
#define u16 __u16
#define u8  __u8
#endif
EOF

%build
export WANT_AUTOCONF_2_5=1
autoconf
%configure --without-ethereal 
#--enable-syspcap
%make
cat <<EOF >README.Mandriva
Since 3.1, kismet changed the configuration format,
especially for the sources naming.

See the list of sources in kis_packsources.cc .

The naming of the rpm is not the same as the upstream
authors. They change so oftern i decided to carry a custom
format for rpm version.
Format of the version is 3.1.YYMMNN with :
YY = Year
MM = Month
NN = Number of version this month

( so feb 2004, first version is 040201 )

This version is labeled  %{name}-%{upstream} on the website.
EOF
%install


rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT

%makeinstall
perl -pi -e 's#/usr/local/#/usr/#' $RPM_BUILD_ROOT/%{_sysconfdir}/kismet.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ -f %{_sysconfdir}/kismet.conf ] ;
then
	if ! egrep -q "^piddir="  %{_sysconfdir}/kismet.conf 
	then 
		echo "piddir=/var/run/" >> %{_sysconfdir}/kismet.conf
	fi
fi

%files
%defattr(-,root,root)
%doc CHANGELOG GPL README TIMESTAMP TODO README.Mandriva 
# kis_packsources.cc is here because it contains the list of sources
%doc docs/DEVEL.* docs/README.* kis_packsources.cc
%config(noreplace) %{_sysconfdir}/kismet.conf
%config(noreplace) %{_sysconfdir}/kismet_ui.conf
%config(noreplace) %{_sysconfdir}/*_manuf
%config(noreplace) %{_sysconfdir}/kismet_drone.conf
%_bindir/*
%_datadir/%name
%_mandir/man1/*
%_mandir/man5/*


