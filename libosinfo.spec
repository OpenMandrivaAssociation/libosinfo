%define oname		osinfo

%define api		1.0
%define major		0
%define libname		%mklibname %{oname} %{api} %{major}
%define develname	%mklibname %{oname} %{api} -d

%define girmajor	1.0
%define girname		%mklibname %{oname}-gir %{girmajor}
%define girnamegtk	%mklibname %{oname}-gtk-gir %{girmajor}

%define _exclude_files_from_autoreq ^%{_datadir}/doc/%{develname}/demo.*$

Summary:	A library for managing OS information for virtualization
Name:		libosinfo
Version:	0.1.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Source0:	https://fedorahosted.org/releases/l/i/libosinfo/%{name}-%{version}.tar.gz
URL:		https://fedorahosted.org/libosinfo/
BuildRequires:	glib2-devel
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(libsoup-2.4)
Requires:	udev

%description
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.


%package common
Summary:	Non-library files for the "%{libname}" library
Group:		System/Libraries

%description common
Platform-independent files for the "%{libname}" library

%files common
%{_bindir}/osinfo-detect
%{_bindir}/osinfo-db-validate
%{_bindir}/osinfo-query
%{_mandir}/man1/osinfo*.1.*
%{_datadir}/libosinfo/db/oses
%{_datadir}/libosinfo/db/*.ids
%{_datadir}/libosinfo/db/devices
%{_datadir}/libosinfo/schemas
%{_datadir}/libosinfo/db/hypervisors
%dir %{_datadir}/libosinfo/db
%dir %{_datadir}/libosinfo/
/lib/udev/rules.d/95-osinfo.rules


%package -n %{libname}
Summary:	Library plugin handling
Group:		System/Libraries
Requires:	%{name}-common = %{version}-%{release}
Provides:	%{mklibname %{oname} %{major}} = %{version}-%{release}

%description -n %{libname}
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

%files -n %{libname}
%{_libdir}/%{name}-%{api}.so.%{major}*


%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %version-%release
Provides:	%{oname}-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files -n %{develname}
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

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/Libosinfo-%{girmajor}.typelib

%prep
%setup -q

%build
%configure2_5x --enable-introspection=yes --enable-vala=yes --enable-udev=yes --disable-static
%make V=1

chmod a-x examples/*.js examples/*.py

%install
%makeinstall_std
rm -f %{buildroot}%{_libdir}/*.la
