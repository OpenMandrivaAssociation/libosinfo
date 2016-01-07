%define oname osinfo
%define api 1.0
%define major 0
%define libname %mklibname %{oname} %{api} %{major}
%define girname %mklibname %{oname}-gir %{api}
%define devname %mklibname %{oname} %{api} -d

%define __no_autoreq '^%{_datadir}/doc/%{devname}/demo.*$'

Summary:	A library for managing OS information for virtualization
Name:		libosinfo
Version:	0.2.12
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://libosinfo.org/
Source0:	https://fedorahosted.org/releases/l/i/libosinfo/%{name}-%{version}.tar.gz
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
Requires:	udev

%track
prog %{name} = {
	url = https://fedorahosted.org/releases/l/i/libosinfo/
	regex = %{name}-(__VER__)\.tar\.gz
	version = %{version}
}

%description
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.


%package common
Summary:	Non-library files for the "%{libname}" library
Group:		System/Libraries

%description common
Platform-independent files for the "%{libname}" library


%package -n %{libname}
Summary:	Library plugin handling
Group:		System/Libraries
Suggests:	%{name}-common = %{version}-%{release}

%description -n %{libname}
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{oname}-devel = %{version}-%{release}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure2_5x \
	--enable-introspection=yes \
	--enable-vala=yes \
	--enable-udev=yes \
	--disable-static
%make

chmod a-x examples/*.js examples/*.py

%install
%makeinstall_std

%find_lang %{name} || touch %{name}.lang

%files common -f %{name}.lang
%{_bindir}/osinfo-detect
%{_bindir}/osinfo-install-script
%{_bindir}/osinfo-db-validate
%{_bindir}/osinfo-query
/lib/udev/rules.d/95-osinfo.rules
%{_datadir}/libosinfo
%{_mandir}/man1/osinfo*.1*

%files -n %{libname}
%{_libdir}/%{name}-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Libosinfo-%{api}.typelib

%files -n %{devname}
%doc AUTHORS ChangeLog COPYING.LIB NEWS README
%doc examples/demo.js
%doc examples/demo.py
%{_libdir}/%{name}-%{api}.so
%dir %{_includedir}/%{name}-%{api}/
%dir %{_includedir}/%{name}-%{api}/osinfo/
%{_includedir}/%{name}-%{api}/osinfo/*.h
%{_libdir}/pkgconfig/%{name}-%{api}.pc
%{_datadir}/gir-1.0/Libosinfo-%{api}.gir
%{_datadir}/gtk-doc/html/Libosinfo
%{_datadir}/vala/vapi/libosinfo-1.0.vapi

