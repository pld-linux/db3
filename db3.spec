Summary:	BSD database library for C
Name:		db3
Version:	3.1.14
Release:	1
Group:		Libraries
License:	GPL
URL:		http://www.sleepycat.com
Source0:	http://www.sleepycat.com/update/%{version}/db-%{version}.tar.gz
#Patch0:	http://www.sleepycat.com/update/%{version}/patch.3.0.55.1
Patch0:		db3-align.patch
Patch1:		db3-linux-threads.patch
Patch2:		db3-shmget.patch
Patch3:		db3-static.patch
PreReq:		/sbin/ldconfig
BuildRequires:	db1-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB is used by many applications,
including Python and Perl, so this should be installed on all systems.

%package utils
Summary:	Command line tools for managing Berkeley DB databases.
Group:		Applications/Databases
Group(pl):	Aplikacje/Bazy danych
Requires:	%{name} = %{version}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching and database
recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB
databases.

%package devel
Summary:	Development libraries and header files for Berkeley database library
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching and database
recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation
for building programs which use Berkeley DB.

%package static
Summary:	Static libraries for Berkeley database library
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching and database
recovery. DB supports C, C++, Java and Perl APIs.

This package contains the static libraries for building programs which use
Berkeley DB.

%prep
%setup -q -n db-%{version}
#%patch0 -p0
#%patch1 -p1
# XXX not applied
#%patch2 -p1
%patch3 -p1

%build
cp -a build_unix build_unix.static

cd build_unix.static

LDFLAGS="-s" \
CFLAGS="$RPM_OPT_FLAGS" \
CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-implicit-templates" \
../dist/configure \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-dump185 \
	--disable-shared \
	--enable-static \
	--enable-rpc \
	--enable-cxx

%{__make} static db_dump185

cd ../build_unix

LDFLAGS="-s" \
CFLAGS="$RPM_OPT_FLAGS" \
CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-implicit-templates" \
../dist/configure \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-shared \
	--disable-static \
	--enable-rpc \
	--enable-cxx \
	--enable-tcl

%{__make} TCFLAGS='-I$(builddir) -I%{_includedir}'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_bindir},/lib}

cd build_unix.static

%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} \
	install_static \
	install_static_cxx

install db_dump185 $RPM_BUILD_ROOT%{_bindir}

cd ../build_unix

%{__make} \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	includedir=$RPM_BUILD_ROOT%{_includedir}/db3 \
	install_include \
	install_dynamic \
	install_dynamic_cxx \
	install_tcl \
	install_utilities

mv $RPM_BUILD_ROOT%{_libdir}/libdb-*.so $RPM_BUILD_ROOT/lib
ln -s ../../lib/libdb-3.1.so $RPM_BUILD_ROOT%{_libdir}/libdb3.so
ln -s libdb-3.1.a $RPM_BUILD_ROOT%{_libdir}/libdb3.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libdb.so

for i in $RPM_BUILD_ROOT%{_prefix}/bin/db_* ; do
	mv $i `echo $i | sed -e 's,/db_,/db3_,'`
done

strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/*
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so

gzip -9nf ../LICENSE ../README

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.gz README.gz
%attr(755,root,root) /lib/libdb-*.so

%files utils
%defattr(644,root,root,755)
%doc docs/utility/*
%attr(755,root,root) %{_libdir}/libdb_tcl-*.so
%attr(755,root,root) %{_bindir}/berkeley_db_svc
%attr(755,root,root) %{_bindir}/db*_archive
%attr(755,root,root) %{_bindir}/db*_checkpoint
%attr(755,root,root) %{_bindir}/db*_deadlock
%attr(755,root,root) %{_bindir}/db*_dump
%attr(755,root,root) %{_bindir}/db*_dump185
%attr(755,root,root) %{_bindir}/db*_load
%attr(755,root,root) %{_bindir}/db*_printlog
%attr(755,root,root) %{_bindir}/db*_recover
%attr(755,root,root) %{_bindir}/db*_stat
%attr(755,root,root) %{_bindir}/db*_upgrade
%attr(755,root,root) %{_bindir}/db*_verify

%files devel
%defattr(644,root,root,755)
%doc docs/{api*,ref,index.html,sleepycat,images} examples*
%attr(755,root,root) %{_libdir}/libdb*.la
%attr(755,root,root) %{_libdir}/libdb3.so
%attr(755,root,root) %{_libdir}/libdb_tcl.so
%attr(755,root,root) %{_libdir}/libdb_cxx*.so
%{_includedir}/db3

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
