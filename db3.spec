Summary:	BSD database library for C
Summary(pl):	Biblioteka C do obs³ugo baz Berkeley DB
Name:		db3
Version:	3.1.17
Release:	8
License:	GPL
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www.sleepycat.com/update/%{version}/db-%{version}.tar.gz
Patch0:		%{name}-static.patch
Patch1:		%{name}-linux.patch
Patch2:		%{name}-jbj.patch
BuildRequires:	db1-static
BuildRequires:	glibc-static
BuildRequires:	tcl-devel >= 8.3.2
URL:		http://www.sleepycat.com/
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

%package tcl
Summary:	Berkeley database library for TCL
Group:		Development/Languages/Tcl
Group(de):	Entwicklung/Sprachen/Tcl
Group(pl):	Programowanie/Jêzyki/Tcl
Requires:	%{name} = %{version}

%description tcl
Berkeley database library for TCL.

%package devel
Summary:	Development libraries and header files for Berkeley database library
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
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
Group(de):	Entwicklung/Libraries
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

This package contains the static libraries for building programs which
use Berkeley DB.

%prep
%setup -q -n db-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -a build_unix build_unix.static

cd build_unix.static

CFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
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

CFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
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
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	install_include \
	install_dynamic \
	install_dynamic_cxx \
	install_tcl \
	install_utilities

mv -f $RPM_BUILD_ROOT%{_libdir}/libdb-*.so $RPM_BUILD_ROOT/lib
ln -sf ../../lib/libdb-3.1.so $RPM_BUILD_ROOT%{_libdir}/libdb.so
ln -sf ../../lib/libdb-3.1.so $RPM_BUILD_ROOT%{_libdir}/libdb3.so
ln -sf ../../lib/libdb-3.1.so $RPM_BUILD_ROOT%{_libdir}/libdb-3.1.so
ln -sf libdb-3.1.a $RPM_BUILD_ROOT%{_libdir}/libdb3.a
ln -sf libdb-3.1.a $RPM_BUILD_ROOT%{_libdir}/libdb.a
ln -sf libdb3.so $RPM_BUILD_ROOT/%{_libdir}/libndbm.so
ln -sf libdb3.a $RPM_BUILD_ROOT/%{_libdir}/libndbm.a

for i in $RPM_BUILD_ROOT%{_bindir}/db_* ; do
	mv -f $i `echo $i | sed -e 's,/db_,/db3_,'`
done

cd ../
rm -rf examples_java
cp -a java/src/com/sleepycat/examples examples_java

gzip -9nf LICENSE README

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   tcl -p /sbin/ldconfig
%postun tcl -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.gz README.gz
%attr(755,root,root) /lib/libdb-*.so

%files utils
%defattr(644,root,root,755)
%doc docs/utility/*
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

%files tcl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdb_tcl-*.so

%files devel
%defattr(644,root,root,755)
%doc docs/{api*,ref,index.html,sleepycat,images} examples*
%attr(755,root,root) %{_libdir}/libdb*.la
%attr(755,root,root) %{_libdir}/libdb.so
%attr(755,root,root) %{_libdir}/libdb3.so
%attr(755,root,root) %{_libdir}/libdb-3.1.so
%attr(755,root,root) %{_libdir}/libndbm.so
%attr(755,root,root) %{_libdir}/libdb_tcl.so
%attr(755,root,root) %{_libdir}/libdb_cxx*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
