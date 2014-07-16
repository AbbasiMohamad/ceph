#
# spec file for package ceph
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%if 0%{defined rhel_version}
%bcond_with gtk2
%else
%bcond_without gtk2
%endif

%if 0%{?jobs} > 6
 %define jobs 6
%endif

# it seems there is no usable tcmalloc rpm for x86_64; parts of
# google-perftools don't compile on x86_64, and apparently the
# decision was to not build the package at all, even if tcmalloc
# itself would have worked just fine.
# Beware: '%bcond_without' turns that feature on!  So as 'osd-mon'
# experiences core-dumps in 'tcmalloc::PageHeap::GrowHeap'...
%bcond_without tcmalloc

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#################################################################################
# common
#################################################################################
Name:           ceph
Version:        0.80.1
Release:        0%{?dist}
Summary:        A Scalable Distributed File System
License:        GPL-2.0 and LGPL-2.1 and Apache-2.0 and MIT and GPL-2.0-with-autoconf-exception
Group:          System/Filesystems
Url:            http://ceph.com/
Source0:        http://ceph.com/download/%{name}-%{version}.tar.bz2
Source1:        README.SUSE.v0.2
Source2:        mkinitrd-root.on.rbd.tar.xz
Source3:        ceph-tmpfiles.d.conf
# filter spurious setgid warning - mongoose/civetweb is not trying to relinquish suid
Source4:        ceph-rpmlintrc
Requires:       cryptsetup
Requires:       libcephfs1 = %{version}-%{release}
Requires:       librados2 = %{version}-%{release}
Requires:       librbd1 = %{version}-%{release}
# python-ceph is used for client tools.
Requires:       python-ceph = %{version}-%{release}
# util-linux because we need mount
Requires:       util-linux
Requires(post): binutils
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if ! 0%{?rhel}
BuildRequires:  sharutils
%endif
%if 0%{?suse_version} < 1310
BuildRequires:  boost49-devel
%else
BuildRequires:  boost-devel > 1.48
%endif
BuildRequires:  gcc-c++
BuildRequires:  gdbm
BuildRequires:  libaio-devel
BuildRequires:  libcurl-devel
BuildRequires:  libedit-devel
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  libxml2-devel
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  python
BuildRequires:  libblkid-devel
BuildRequires:  snappy-devel
BuildRequires:  leveldb-devel
BuildRequires:  xfsprogs-devel
BuildRequires:  xz
%if 0%{?suse_version} >= 1310
BuildRequires:  systemd
%endif
# This patch queue is auto-generated from https://github.com/SUSE/ceph
Patch0001:      0001-Rcfiles-remove-from-runlevel-2.patch
Patch0002:      0002-init-radosgw-adjust-for-opensuse.patch
Patch0003:      0003-mkcephfs-add-xfs-support.patch
Patch0004:      0004-init-ceph-add-xfs-support.patch
Patch0005:      0005-Fix-runlevels-for-start-scripts.patch
Patch0006:      0006-Drop-ceph-keys-into-install.patch
Patch0007:      0007-add-syncfs-support-v3.patch
Patch0008:      0008-Fixup-radosgw-daemon-init.patch
# Please do not add patches manually here, run update_git.sh.

#################################################################################
# specific
#################################################################################
%if 0%{defined suse_version}
# ceph-disk uses gptfdisk to format OSD disks
Requires:       gptfdisk
BuildRequires:  %insserv_prereq
Recommends:     logrotate
BuildRequires:  keyutils-devel
BuildRequires:  libatomic-ops-devel
BuildRequires:  mozilla-nss-devel
%else
BuildRequires:  keyutils-libs-devel
BuildRequires:  libatomic_ops-devel
BuildRequires:  nss-devel
Requires:       gdisk
Requires(post): chkconfig
Requires(preun):chkconfig
Requires(preun):initscripts
%endif
%ifnarch ppc ppc64 s390 s390x ia64
%if 0%{?suse_version} >= 1310
%if 0%{with tcmalloc}
# use isa so this will not be satisfied by
# google-perftools-devel.i686 on a x86_64 box
# http://rpm.org/wiki/PackagerDocs/ArchDependencies
BuildRequires:  gperftools-devel%{?_isa}
%endif
%endif
%endif

%description
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability.

#################################################################################
# packages
#################################################################################
%package fuse
Summary:        Ceph fuse-based client
License:        GPL-2.0 and LGPL-2.1
Group:          System/Filesystems
Requires:       %{name} = %{version}-%{release}
BuildRequires:  fuse-devel

%description fuse
FUSE based client for Ceph distributed network file system

%if 0%{?rbd_fuse}

%package -n rbd-fuse
Summary:        RBD fuse-based client
License:        GPL-2.0 and LGPL-2.1 and Apache-2.0 and MIT and GPL-2.0-with-autoconf-exception
Group:          System/Filesystems
Requires:       %{name} = %{version}-%{release}
BuildRequires:  fuse-devel

%description -n rbd-fuse
FUSE based client for Ceph distributed network file system

%endif

%package devel
Summary:        Ceph headers
License:        GPL-2.0 and LGPL-2.1
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Requires:       librados2 = %{version}
Requires:       librbd1 = %{version}
Requires:       libcephfs1 = %{version}

%description devel
This package contains libraries and headers needed to develop programs
that use Ceph.

%package radosgw
Summary:        Rados REST Gateway
License:        GPL-2.0 and LGPL-2.1
Group:          System/Filesystems
Requires:       librados2 = %{version}-%{release}
Requires:       logrotate
%if 0%{defined suse_version}
BuildRequires:  FastCGI-devel
BuildRequires:  libexpat-devel
Requires:       apache2-mod_fcgid
%else
BuildRequires:  expat-devel
BuildRequires:  fcgi-devel
Requires:       mod_fcgid

%endif
%description radosgw
radosgw is an S3 HTTP REST gateway for the RADOS object store. It is
implemented as a FastCGI module using libfcgi, and can be used in
conjunction with any FastCGI capable web server.

%if 0%{?suse_version}
%package resource-agents
Summary:        OCF-compliant Resource Agents for Ceph Daemons
License:        GPL-2.0 and LGPL-2.1
Group:          System/Filesystems
Requires:       %{name} = %{version}
Requires:       resource-agents

%description resource-agents
Resource agents for monitoring and managing Ceph daemons
under Open Cluster Framework (OCF) compliant resource
managers such as Pacemaker.
%endif

%package -n librados2
Summary:        RADOS distributed object store client library
License:        GPL-2.0 and LGPL-2.1
Group:          System/Filesystems

%description -n librados2
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n librbd1
Summary:        RADOS Block Device Client Library
License:        GPL-2.0 and LGPL-2.1
Group:          System/Filesystems
Requires:       librados2 = %{version}-%{release}

%description -n librbd1
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n libcephfs1
Summary:        Ceph distributed file system client library
Group:          System/Filesystems
License:        LGPL-2.1 and BSD-2-Clause and GPL-2.0

%description -n libcephfs1
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%if 0%{?cephfs_java}
%package -n libcephfs_jni1
Summary:        Java Native Interface library for CephFS Java bindings
License:        GPL-2.0 and LGPL-2.1 and Apache-2.0 and MIT and GPL-2.0-with-autoconf-exception
Group:          System/Filesystems
Requires:       java
%if 0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  java-1.6.0-openjdk-devel
%else
%if 0%{?fedora}
BuildRequires:  java-1.7.0-openjdk-devel
%else
BuildRequires:  java-devel
%endif
%endif

%description -n libcephfs_jni1
This package contains the Java Native Interface library for CephFS Java
bindings.

%package -n cephfs-java
Summary:        Java libraries for the Ceph File System
License:        GPL-2.0 and LGPL-2.1 and Apache-2.0 and MIT and GPL-2.0-with-autoconf-exception
Group:          System/Filesystems
Requires:       java
%if 0%{?suse_version} > 1220
Requires:       junit4
BuildRequires:  junit4
%endif
Requires:       libcephfs_jni1 = %{version}-%{release}
%if 0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  java-1.6.0-openjdk-devel
%else
%if 0%{?fedora}
BuildRequires:  java-1.7.0-openjdk-devel
%else
BuildRequires:  java-devel
%endif
%endif

%description -n cephfs-java
This package contains the Java libraries for the Ceph File System.

%endif

%package -n python-ceph
Summary:        Python Libraries for the Ceph Distributed Filesystem
License:        GPL-2.0 and LGPL-2.1
Group:          System/Filesystems
Requires:       libcephfs1 = %{version}-%{release}
Requires:       librados2 = %{version}-%{release}
Requires:       librbd1 = %{version}-%{release}
%if 0%{defined suse_version}
%py_requires
%endif

%description -n python-ceph
This package contains Python libraries for interacting with Cephs RADOS
object storage.

%package -n ceph-test
Summary:        Ceph benchmarks and test tools
License:        GPL-2.0 and LGPL-2.1 and Apache-2.0 and MIT and GPL-2.0-with-autoconf-exception
Group:          System/Filesystems
Requires:       libcephfs1 = %{version}-%{release}
Requires:       librados2 = %{version}-%{release}
Requires:       librbd1 = %{version}-%{release}

%description -n ceph-test
This package contains Ceph benchmarks and test tools.


#################################################################################
# common
#################################################################################
%prep
%setup -q
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1

%build

# Find jni.h
for i in /usr/{lib64,lib}/jvm/java/include{,/linux}; do
    echo $i
    [ -d $i ] && java_inc="$java_inc -I$i"
done

./autogen.sh

export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/i386/i486/'`

# be explicit about --with/without-tcmalloc because the
# autoconf default differs from what's needed for rpm
#
# Prefix with CXXFLAGS="-g -pg" to remove optimisation.
%{configure}    CPPFLAGS="$java_inc" \
                --disable-static \
                --localstatedir=/var \
                --sysconfdir=/etc \
                --docdir=%{_docdir}/ceph \
                --without-hadoop \
                --with-radosgw \
                --with-nss \
                --with-rest-bench \
                --with-debug=yes \
%if 0%{?cephfs_java}
                --enable-cephfs-java \
%endif
%if 0%{?suse_version}
                --with-ocf \
%endif
%if 0%{with system_leveldb}
                --with-system-leveldb \
%else
                --without-system-leveldb \
%endif
%ifnarch ppc ppc64 s390 s390x ia64
%if 0%{?suse_version} >= 1310
%if 0%{with tcmalloc}
                --with-tcmalloc \
%else
                --without-tcmalloc \
%endif
%else
                --without-tcmalloc \
%endif
%else
                --without-tcmalloc \
%endif
                CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"

# fix bug in specific version of libedit-devel
%if 0%{defined suse_version}
sed -i -e "s/-lcurses/-lncurses/g" Makefile
sed -i -e "s/-lcurses/-lncurses/g" src/Makefile
sed -i -e "s/-lcurses/-lncurses/g" man/Makefile
sed -i -e "s/-lcurses/-lncurses/g" src/ocf/Makefile
sed -i -e "s/-lcurses/-lncurses/g" src/java/Makefile
grep "\-lcurses" * -R
%endif

make %{?jobs:-j%{jobs}}

#cd src/gtest
#echo "------ MAKE GTEST ------"
#make -j$(getconf _NPROCESSORS_ONLN)
#cd ..
#echo "------ MAKE UNITTEST ------"
#make unittests -j$(getconf _NPROCESSORS_ONLN)
#echo "------ MAKE ... DONE ------"

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
install -D src/init-ceph $RPM_BUILD_ROOT%{_initrddir}/ceph
install -D src/init-radosgw $RPM_BUILD_ROOT%{_initrddir}/ceph-radosgw
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
ln -sf ../../etc/init.d/ceph %{buildroot}/%{_sbindir}/rcceph
ln -sf ../../etc/init.d/ceph-radosgw %{buildroot}/%{_sbindir}/rcceph-radosgw
install -m 0644 -D src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph
install -m 0644 -D src/rgw/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph-radosgw
chmod 0644 $RPM_BUILD_ROOT%{_docdir}/ceph/sample.ceph.conf
chmod 0644 $RPM_BUILD_ROOT%{_docdir}/ceph/sample.fetch_config

# udev rules
install -m 0644 -D udev/50-rbd.rules $RPM_BUILD_ROOT/lib/udev/rules.d/50-rbd.rules
install -m 0644 -D udev/95-ceph-osd.rules $RPM_BUILD_ROOT/lib/udev/rules.d/95-ceph-osd.rules

#set up placeholder directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/tmp/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/ceph/
%if 0%{?suse_version} >= 1310
%{__install} -d -m 0755 %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/%{name}.conf
%else
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/ceph/
%endif
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ceph/
cp %{S:1} $RPM_BUILD_ROOT/%{_docdir}/ceph/README.SUSE
rm $RPM_BUILD_ROOT%{python_sitelib}/*.pyo
rm -f $RPM_BUILD_ROOT/usr/share/ceph/id_dsa_drop.ceph.com
rm -f $RPM_BUILD_ROOT/usr/share/ceph/id_dsa_drop.ceph.com.pub
rm -f $RPM_BUILD_ROOT/usr/share/ceph/known_hosts_drop.ceph.com
mkdir $RPM_BUILD_ROOT/var/lib/ceph/osd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%if 0%{?suse_version} >= 1310
systemd-tmpfiles --create %{_tmpfilesdir}/%{name}.conf
%endif
#/sbin/chkconfig --add ceph

%preun
%if %{defined suse_version}
%stop_on_removal ceph
%endif
%if 0%{?suse_version} < 1310
if [ $1 = 0 ] ; then
    /sbin/service ceph stop >/dev/null 2>&1
#    /sbin/chkconfig --del ceph
fi
%endif
%postun
/sbin/ldconfig
if [ "$1" -ge "1" ] ; then
    /sbin/service ceph condrestart >/dev/null 2>&1 || :
fi
%if %{defined suse_version}
%restart_on_update ceph
%insserv_cleanup
%endif

#################################################################################
# files
#################################################################################
%files
%defattr(-,root,root,-)
%docdir %{_docdir}
%dir %{_docdir}/ceph
%{_docdir}/ceph/sample.ceph.conf
%{_docdir}/ceph/sample.fetch_config
%{_docdir}/ceph/README.SUSE
%{_bindir}/ceph
%{_bindir}/cephfs
%{_bindir}/ceph-conf
%{_bindir}/ceph-clsinfo
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-authtool
%{_bindir}/ceph-syn
%{_bindir}/ceph-run
%{_bindir}/ceph-mon
%{_bindir}/ceph-mds
%{_bindir}/ceph-osd
%{_bindir}/ceph-post-file
%{_bindir}/ceph-rest-api
%{_bindir}/ceph-rbdnamer
%{_bindir}/ceph_filestore_dump
%{_bindir}/ceph_filestore_tool
%{_bindir}/librados-config
%{_bindir}/rados
%{_bindir}/rbd
%{_bindir}/ceph-coverage
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-brag
%{_bindir}/ceph-crush-location
%{_bindir}/ceph-monstore-tool
%{_bindir}/ceph-osdomap-tool
%{_bindir}/ceph_mon_store_converter
%{_bindir}/ceph_erasure_code
%{_initrddir}/ceph
/sbin/mkcephfs
/sbin/mount.ceph
%{_sbindir}/ceph-disk
%{_sbindir}/ceph-disk-prepare
%{_sbindir}/ceph-disk-activate
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk-udev
%{_sbindir}/rcceph

%dir %{_libdir}/rados-classes
%{_libdir}/rados-classes/libcls_kvs.so*
%{_libdir}/rados-classes/libcls_lock.so*
%{_libdir}/rados-classes/libcls_log.so*
%{_libdir}/rados-classes/libcls_rbd.so*
%{_libdir}/rados-classes/libcls_refcount.so*
%{_libdir}/rados-classes/libcls_replica_log.so*
%{_libdir}/rados-classes/libcls_rgw.so*
%{_libdir}/rados-classes/libcls_statelog.so*
%{_libdir}/rados-classes/libcls_version.so*
%{_libdir}/rados-classes/libcls_hello.so*
%{_libdir}/rados-classes/libcls_user.so*

%{_libdir}/ceph
%dir /lib/udev
%dir /lib/udev/rules.d
/lib/udev/rules.d/50-rbd.rules
/lib/udev/rules.d/95-ceph-osd.rules
%config %{_sysconfdir}/bash_completion.d/ceph
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/radosgw-admin
%config %{_sysconfdir}/bash_completion.d/rbd
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%{_mandir}/man8/ceph-mon.8*
%{_mandir}/man8/ceph-mds.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/mkcephfs.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/cephfs.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/rbd.8*
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-clsinfo.8.gz
%{_mandir}/man8/librados-config.8.gz
%{_mandir}/man8/ceph-dencoder.8.gz
%{_mandir}/man8/ceph-rbdnamer.8.gz
%{_mandir}/man8/ceph-post-file.8.gz
%{_mandir}/man8/ceph-rest-api.8.gz
%dir %{_localstatedir}/lib/ceph/
%dir %{_localstatedir}/lib/ceph/tmp/
%dir %{_localstatedir}/log/ceph/
%if 0%{?suse_version} < 1310
%ghost %dir %{_localstatedir}/run/ceph/
%else
%dir %{_tmpfilesdir}/
%{_tmpfilesdir}/%{name}.conf
%endif
%dir %{_sysconfdir}/ceph/
# osd mounting directory
%dir /var/lib/ceph/osd

#################################################################################
%files fuse
%defattr(-,root,root,-)
%{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*
/sbin/mount.fuse.ceph
%{_bindir}/rbd-fuse
%{_mandir}/man8/rbd-fuse.8*

%if 0%{?rbd_fuse}
%files -n rbd-fuse
%defattr(-,root,root,-)
%endif




#################################################################################
%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/libcephfs.h
%dir %{_includedir}/rados
%{_includedir}/rados/memory.h
%{_includedir}/rados/librados.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/rados_types.h
%{_includedir}/rados/buffer.h
%{_includedir}/rados/page.h
%{_includedir}/rados/crc32c.h
%{_includedir}/rados/rados_types.hpp
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/libcephfs.so
%{_libdir}/librbd.so
%{_libdir}/librados.so

#################################################################################
%files radosgw
%defattr(-,root,root,-)
%{_initrddir}/ceph-radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-admin
%{_mandir}/man8/radosgw.8*
%{_mandir}/man8/radosgw-admin.8*
%{_sbindir}/rcceph-radosgw
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph-radosgw

%post radosgw
/sbin/ldconfig
%if %{defined suse_version}
%fillup_and_insserv -f -y ceph-radosgw
%endif

%preun radosgw
%if %{defined suse_version}
%stop_on_removal ceph-radosgw
%endif

%postun radosgw
/sbin/ldconfig
%if %{defined suse_version}
%restart_on_update ceph-radosgw
%insserv_cleanup
%endif


#################################################################################
%if 0%{?suse_version}

%files resource-agents
%defattr(0755,root,root,-)
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
%dir /usr/lib/ocf/resource.d/ceph
/usr/lib/ocf/resource.d/%{name}/*
%endif

#################################################################################
%files -n librados2
%defattr(-,root,root,-)
%{_libdir}/librados.so.*

%post -n librados2
/sbin/ldconfig

%postun -n librados2
/sbin/ldconfig

#################################################################################
%files -n librbd1
%defattr(-,root,root,-)
%{_libdir}/librbd.so.*

%post -n librbd1
/sbin/ldconfig

%postun -n librbd1
/sbin/ldconfig

#################################################################################

%files -n libcephfs1
%defattr(-,root,root,-)
%{_libdir}/libcephfs.so.*

%post -n libcephfs1
/sbin/ldconfig

%postun -n libcephfs1
/sbin/ldconfig

#################################################################################
%if 0%{?cephfs_java}
%files -n libcephfs_jni1
%defattr(-,root,root,-)
%{_libdir}/libcephfs_jni.so.*

%post -n libcephfs_jni1
/sbin/ldconfig

%postun -n libcephfs_jni1
/sbin/ldconfig

#################################################################################
%files -n cephfs-java
%defattr(-,root,root,-)
%if 0%{?suse_version} > 1220 
%{_javadir}/libcephfs-test.jar
%endif
%{_javadir}/libcephfs.jar
%endif

#################################################################################
%files -n python-ceph
%defattr(-,root,root,-)
%{python_sitelib}/ceph_argparse.py*
%{python_sitelib}/ceph_rest_api.py*
%{python_sitelib}/cephfs.py*
%{python_sitelib}/rados.py*
%{python_sitelib}/rbd.py*

%files -n ceph-test
%defattr(-,root,root,-)
%{_bindir}/rest-bench
%{_bindir}/ceph_bench_log
%{_bindir}/ceph_dupstore
%{_bindir}/ceph_erasure_code_benchmark
%{_bindir}/ceph_kvstorebench
%{_bindir}/ceph_multi_stress_watch
%{_bindir}/ceph_omapbench
%{_bindir}/ceph_psim
%{_bindir}/ceph_radosacl
%{_bindir}/ceph_rgw_jsonparser
%{_bindir}/ceph_rgw_multiparser
%{_bindir}/ceph_scratchtool
%{_bindir}/ceph_scratchtoolpp
%{_bindir}/ceph_smalliobench
%{_bindir}/ceph_smalliobenchrbd
%{_bindir}/ceph_smalliobenchdumb
%{_bindir}/ceph_smalliobenchfs
%{_bindir}/ceph_streamtest
%{_bindir}/ceph_test_cfuse_cache_invalidate
%{_bindir}/ceph_test_cls_hello
%{_bindir}/ceph_test_cls_lock
%{_bindir}/ceph_test_cls_log
%{_bindir}/ceph_test_cls_rbd
%{_bindir}/ceph_test_cls_refcount
%{_bindir}/ceph_test_cls_replica_log
%{_bindir}/ceph_test_cls_rgw
%{_bindir}/ceph_test_cls_rgw_log
%{_bindir}/ceph_test_cls_rgw_meta
%{_bindir}/ceph_test_cls_rgw_opstate
%{_bindir}/ceph_test_cls_statelog
%{_bindir}/ceph_test_cls_version
%{_bindir}/ceph_test_msgr
%{_bindir}/ceph_test_rados
%{_bindir}/ceph_test_rados_api_cmd
%{_bindir}/ceph_test_rados_api_lock
%{_bindir}/ceph_test_snap_mapper
%{_bindir}/ceph_test_filejournal
%{_bindir}/ceph_test_filestore_idempotent
%{_bindir}/ceph_test_filestore_idempotent_sequence
%{_bindir}/ceph_test_ioctls
%{_bindir}/ceph_test_keyvaluedb_atomicity
%{_bindir}/ceph_test_keyvaluedb_iterators
%{_bindir}/ceph_test_libcephfs
%{_bindir}/ceph_test_librbd
%{_bindir}/ceph_test_librbd_fsx
%{_bindir}/ceph_test_mon_workloadgen
%{_bindir}/ceph_test_mutate
%{_bindir}/ceph_test_object_map
%{_bindir}/ceph_test_objectcacher_stress
%{_bindir}/ceph_test_rados_api_aio
%{_bindir}/ceph_test_rados_api_c_read_operations
%{_bindir}/ceph_test_rados_api_c_write_operations
%{_bindir}/ceph_test_rados_api_cls
%{_bindir}/ceph_test_rados_api_io
%{_bindir}/ceph_test_rados_api_list
%{_bindir}/ceph_test_rados_api_misc
%{_bindir}/ceph_test_rados_api_pool
%{_bindir}/ceph_test_rados_api_snapshots
%{_bindir}/ceph_test_rados_api_stat
%{_bindir}/ceph_test_rados_api_tier
%{_bindir}/ceph_test_rados_api_watch_notify
%{_bindir}/ceph_test_rewrite_latency
%{_bindir}/ceph_test_stress_watch
%{_bindir}/ceph_test_trans
%{_bindir}/ceph_test_c_headers
%{_bindir}/ceph_test_cors
%{_bindir}/ceph_test_crypto
%{_bindir}/ceph_test_get_blkdev_size
%{_bindir}/ceph_test_keys
%{_bindir}/ceph_test_objectstore
%{_bindir}/ceph_test_objectstore_workloadgen
%{_bindir}/ceph_test_rados_delete_pools_parallel
%{_bindir}/ceph_test_rados_list_parallel
%{_bindir}/ceph_test_rados_open_pools_parallel
%{_bindir}/ceph_test_rados_watch_notify
%{_bindir}/ceph_test_rgw_manifest
%{_bindir}/ceph_test_signal_handlers
%{_bindir}/ceph_test_timers
%{_bindir}/ceph_tpbench
%{_bindir}/ceph_xattr_bench
%{_bindir}/ceph-kvstore-tool
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-client-debug
%{_mandir}/man8/ceph-debugpack.8*

%changelog
