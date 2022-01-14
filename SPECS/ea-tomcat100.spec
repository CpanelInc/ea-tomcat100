%global ns_dir /opt/cpanel

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

%if 0%{?centos} >= 7 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

%if 0%{?rhel} >= 8
%global debug_package %{nil}
%endif

Name:    ea-tomcat100
Vendor:  cPanel, Inc.
Summary: Tomcat
Version: 10.0.14
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: Apache License, 2.0
Group:   System Environment/Daemons
URL: http://tomcat.apache.org/
Source0: https://www-us.apache.org/dist/tomcat/tomcat-8/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1: setenv.sh
Source2: sample.ea-tomcat100.logrotate
Source3: sample.ea-tomcat100.service
Source4: sample.ea-tomcat100.initd
Source5: cpanel-scripts-ea-tomcat100
Source7: README.FASTERSTARTUP
Source8: README.SECURITY
Source9: README.USER-SERVICE-MANAGEMENT
Source10: user-init.sh
Source11: user-setenv.sh
Source12: user-shutdown.sh
Source13: user-startup.sh
Source14: README.APACHE-PROXY
Source15: README.USER-INSTANCE
Source16: test.jsp
Source17: README.SHARED-SERVICE-MANAGEMENT

# if I do not have autoreq=0, rpm build will recognize that the ea_
# scripts need perl and some Cpanel pm's to be on the disk.
# unfortunately they cannot be satisfied via the requires: tags.
Autoreq: 0

Requires: ea-apache24-mod_proxy_ajp

# Create Tomcat user/group as we definitely do not want this running as root.
Requires(pre): /usr/sbin/useradd, /usr/bin/getent

%if %{with_systemd}
BuildRequires: systemd-units
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# For triggerun
Requires(post): systemd-sysv
%else
BuildRequires: chkconfig
Requires: initscripts
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%endif
Requires(pre):  shadow-utils

Requires:       ea-podman

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%prep
%setup -qn apache-tomcat-%{version}

%pre

# add the group if we need it:
if [ $(/usr/bin/getent group tomcat | wc -c) -eq 0 ];
    then /usr/sbin/groupadd -r tomcat;
fi

# if the user already exists, just add to group
if [ $(/usr/bin/getent passwd tomcat | wc -c) -ne 0 ];
    then usermod -g tomcat tomcat;
else
# otherwise lets just create the user like normal
    /usr/sbin/useradd -r -d /opt/cpanel/%{name} -s /sbin/nologin -g tomcat tomcat
fi

if [ -x "/usr/local/cpanel/scripts/ea-tomcat100" ]; then
    /usr/local/cpanel/scripts/ea-tomcat100 all stop
fi

%build
# empty build section

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100
cp -r ./* $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100
cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/bin/
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/
cp %{SOURCE3} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/
cp %{SOURCE4} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/
cp /etc/rc.d/init.d/functions $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/bin/user-functions

# put logs under /var/log ...
mkdir -p $RPM_BUILD_ROOT/var/log/ea-tomcat100
rmdir $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/logs
ln -sf /var/log/ea-tomcat100 $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/logs

ln -sf /var/run $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/run

mkdir -p $RPM_BUILD_ROOT/var/run/ea-tomcat100

mkdir -p $RPM_BUILD_ROOT/usr/local/cpanel/scripts
cp %{SOURCE5} $RPM_BUILD_ROOT/usr/local/cpanel/scripts/ea-tomcat100

# private instance items
cp %{SOURCE7} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.FASTERSTARTUP
cp %{SOURCE8} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.SECURITY
cp %{SOURCE9} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.USER-SERVICE-MANAGEMENT
cp %{SOURCE14} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.APACHE-PROXY
cp %{SOURCE15} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.USER-INSTANCE
cp %{SOURCE16} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/test.jsp
cp %{SOURCE17} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.SHARED-SERVICE-MANAGEMENT

cp %{SOURCE10} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/bin/user-init.sh
cp %{SOURCE11} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/bin/user-setenv.sh
cp %{SOURCE12} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/bin/user-shutdown.sh
cp %{SOURCE13} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/bin/user-startup.sh

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/user-conf
cp -r ./conf/* $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/user-conf

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%preun
/usr/local/cpanel/scripts/ea-tomcat100 all stop

%posttrans
if [ -x "/usr/local/cpanel/scripts/ea-tomcat100" ]; then
    /usr/local/cpanel/scripts/ea-tomcat100 all restart
fi

%files
%attr(0755,root,root) /usr/local/cpanel/scripts/ea-tomcat100
%defattr(-,root,tomcat,-)
/opt/cpanel/ea-tomcat100
%attr(0755,root,root) /opt/cpanel/ea-tomcat100/user-conf
%attr(0644,root,root) /opt/cpanel/ea-tomcat100/README*
%attr(0644,root,root) /opt/cpanel/ea-tomcat100/sample*
%attr(0755,root,root) /opt/cpanel/ea-tomcat100/bin/user-*
%config(noreplace) %attr(0755,root,tomcat) /opt/cpanel/ea-tomcat100/bin/setenv.sh
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/server.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/context.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/jaspic-providers.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/jaspic-providers.xsd
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/tomcat-users.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/tomcat-users.xsd
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/web.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/catalina.policy
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/catalina.properties
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/conf/logging.properties
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/webapps/ROOT/WEB-INF/web.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/webapps/manager/META-INF/context.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/webapps/manager/WEB-INF/web.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/webapps/host-manager/META-INF/context.xml
%config(noreplace) %attr(0640,root,tomcat) /opt/cpanel/ea-tomcat100/webapps/host-manager/WEB-INF/web.xml

%dir /var/log/ea-tomcat100
%dir %attr(0770,root,tomcat) /var/run/ea-tomcat100
%ghost %attr(0640,tomcat,tomcat) /var/run/ea-tomcat100/catalina.pid

%changelog
* Fri Jan 14 2022 Julian Brown <julian.brown@webpros.com> - 10.0.14-1
- ZC-9647: Initial Build of tomcat 10.0 using podman

