Summary:	Berkeley DB
Name:		db
Version:	3.0.55
Release:	1
License:	distributable
Group:		Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	%{name}-%{version}.tar.gz
Patch0:		db3-DESTDIR.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	%{_prefix}/include/db3

%description

%package devel
Summary:	Berkeley DB
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel

#%package static
#Summary:	Berkeley DB
#Group:		Development/Libraries
#Group(fr):	Development/Librairies
#Group(pl):	Programowanie/Biblioteki
#Requires:	%{name}-devel = %{version}
#
#%description static

%prep
%setup -q
chmod -R u+w *
%patch0 -p1 

%build
LDFLAGS="-s"; export LDFLAGS
cd dist
%configure \
	--enable-compat185 \
	--enable-cxx \
	--enable-dynamic \
	--enable-shared \
	--enable-static \
	--enable-tcl

make

%install
rm -rf $RPM_BUILD_ROOT

cd dist
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/doc/%{name}-%{version}

cd $RPM_BUILD_ROOT%{_bindir}
for i in `ls`; do
	mv $i `echo $i|sed -e 's/^db/db3/'`;
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libdb*-3*.so

%files devel
%defattr(644,root,root,755)
%doc %{_datadir}/doc/%{name}-%{version}
%{_includedir}

#%files static
#%defattr(644,root,root,755)
