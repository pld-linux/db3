%define	__soversion	3.1
%define	_libdb_a	libdb-%{__soversion}.a

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
PreReq:		/sbin/ldconfig

# XXX written as a file prereq in order to build with glibc-2.1.3
%ifos linux
BuildPrereq:	/usr/lib/libdb1.a
%endif

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
#%patch1 -p1

%build

cd build_unix

# XXX --enable-tcl can't add without picking up dependency on libtcl.so
# XXX --enable-posixmutexes (missing pthread_{cond,mutex}attr_setpshared)
# XXX --enable-cxx (barfs on clone proto in %{_includedir}/bits/sched.h)
# XXX --enable-debug_{r,w}op should be disabled for production.
CFLAGS="$RPM_OPT_FLAGS" ../dist/configure --prefix=%{_prefix} --enable-debug --enable-compat185 --enable-diagnostic --enable-dump185 --enable-shared --enable-static --enable-rpc --enable-tcl # --enable-test --enable-debug --enable-debug_rop --enable-debug_wop # --enable-posixmutexes

%{__make} libdb=%{_libdb_a} %{_libdb_a}

# Static link with old db-185 libraries.
/bin/sh ./libtool --mode=compile cc -c -O2 -g -g -I%{_includedir}/db1 -I../dist/../include -D_REENTRANT  ../dist/../db_dump185/db_dump185.c
cc -s -static -o db_dump185 db_dump185.lo -L%{_libdir} -ldb1

# Compile rest normally.
%{__make} libdb=%{_libdb_a} TCFLAGS='-I$(builddir) -I%{_includedir}' LDFLAGS="-s"

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_includedir}
install -d ${RPM_BUILD_ROOT}%{_libdir}

cd build_unix

# XXX install_tcl
# XXX install_static_cxx
# XXX install_dynamic_cxx
# XXX install_java
# XXX install_docs (handled by %docs)
%{__make} libdb=%{_libdb_a} LDFLAGS="-s" prefix=${RPM_BUILD_ROOT}%{_prefix} install_include install_dynamic install_static install_tcl install_utilities

# XXX annoying
set -x
( cd ${RPM_BUILD_ROOT}

%ifos linux
  install -d ./lib
  mv -f .%{_libdir}/libdb[-.]*so* ./lib
  if [ "%{_libdir}" != "%{_libdir}" ]; then
    install -d .%{_libdir}
    mv -f .%{_libdir}/libdb* .%{_libdir}
  fi
%endif

  mkdir -p .%{_includedir}/db3
  mv -f .%{_prefix}/include/*.h .%{_includedir}/db3
  ln -sf db3/db.h .%{_includedir}/db.h
#  for F in .%{_prefix}/bin/db_* ; do
#    mv $F `echo $F | sed -e 's,/db_,/db3_,'`
#  done
)
set +x

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README docs/images
%ifos linux
/lib/libdb-%{__soversion}.so
%else
%{_libdir}/libdb-%{__soversion}.so
%endif

%files utils
%defattr(644,root,root,755)
%doc docs/utility
%{_libdir}/libdb_tcl-%{__soversion}.so
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
%doc	docs/api_c docs/api_cxx docs/api_java docs/api_tcl docs/index.html
%doc	docs/ref docs/sleepycat
%doc	examples_c examples_cxx
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/libdb_tcl-%{__soversion}.la
%{_libdir}/%{_libdb_a}
%{_includedir}/db3/db.h
%{_includedir}/db3/db_185.h
%{_includedir}/db3/db_cxx.h
%{_includedir}/db.h
%ifos linux
/lib/libdb.so
%else
%{_libdir}/libdb.so
%endif
%{_libdir}/libdb_tcl.so

%files static
%defattr(644,root,root,755)
%{_libdir}/%{_libdb_a}
