%define oname osinfo
%define api 1.0
%define major 0
%define libname %mklibname %{oname} %{api} %{major}
%define girname %mklibname %{oname}-gir %{api}
%define devname %mklibname %{oname} %{api} -d

%global __requires_exclude_from '^%{_datadir}/doc/%{devname}/demo.*$'

Summary:	A library for managing OS information for virtualization
Name:		libosinfo
Version:	1.7.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://libosinfo.org/
Source0:	https://releases.pagure.org/libosinfo/%{name}-%{version}.tar.xz
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	meson
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	osinfo-db
Requires:	udev
Requires:	osinfo-db
Requires:	osinfo-db-tools

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

%package vala
Summary: Vala bindings
Group: Development/Other
Requires: %{name}-common = %{version}-%{release}

%description vala
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

This package provides the Vala bindings for libosinfo library.

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
%autosetup -p1

%build
%meson -Denable-gtk-doc=false
%meson_build

%install
%meson_install

%find_lang %{name} || touch %{name}.lang

%files common -f %{name}.lang
%{_bindir}/osinfo-detect
%{_bindir}/osinfo-install-script
%{_bindir}/osinfo-query
%{_mandir}/man1/osinfo*.1*

%files -n %{libname}
%{_libdir}/%{name}-%{api}.so.%{major}*

%files vala
%{_datadir}/vala/vapi/libosinfo-1.0.*

%files -n %{girname}
%{_libdir}/girepository-1.0/Libosinfo-%{api}.typelib

%files -n %{devname}
%doc AUTHORS ChangeLog COPYING.LIB NEWS README
%{_libdir}/%{name}-%{api}.so
%dir %{_includedir}/%{name}-%{api}/
%dir %{_includedir}/%{name}-%{api}/osinfo/
%{_includedir}/%{name}-%{api}/osinfo/*.h
%{_libdir}/pkgconfig/%{name}-%{api}.pc
%{_datadir}/gir-1.0/Libosinfo-%{api}.gir
