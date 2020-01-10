%define oversion 2011-03-R2
%define version %(echo %{oversion}| tr - .)

Summary:	802.11b/g network sniffer and network dissector
Name:		kismet
Version:	%{version}
Release:	3
License:	GPLv2+
Group:		Networking/Other
Url:		http://www.kismetwireless.net
Source0:	http://www.kismetwireless.net/code/%{name}-%{oversion}.tar.gz
Patch1:		kismet-2009-06-R1-envp.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	wget
BuildRequires:	gmp-devel
BuildRequires:	pcap-devel
BuildRequires:	pkgconfig(libgpsd)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(ImageMagick)
BuildRequires:	pkgconfig(ncurses)
Requires:	wget
Requires:	wireless-tools

%description
Kismet is an 802.11b/g network sniffer and network dissector. It is
capable of sniffing using most wireless cards, automatic network IP
block detection via UDP, ARP, and DHCP packets, Cisco equipment lists
via Cisco Discovery Protocol, weak cryptographic packet logging, and
Ethereal and tcpdump compatible packet dump files. It also includes
the ability to plot detected networks and estimated network ranges on
downloaded maps or user supplied image files.

%files
%doc CHANGELOG GPL README
%doc docs/DEVEL.* docs/README.*
%config(noreplace) %{_sysconfdir}/kismet.conf
%config(noreplace) %{_sysconfdir}/kismet_drone.conf
%{_bindir}/*
%{_datadir}/%{name}/
%{_mandir}/man1/*
%{_mandir}/man5/*

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}-%{oversion}
%autopatch -p1

sed -i 's#\$(prefix)/lib/#%{_libdir}/#g' plugin-*/Makefile

%build
export LDFLAGS="-Wl,--as-needed"
%configure2_5x \
    CXXFLAGS="%{optflags} -D__STDC_FORMAT_MACROS"

%make

%install
%makeinstall_std INSTUSR="$(id -un)" INSTGRP="$(id -gn)" MANGRP="$(id -gn)"

