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

Name:    ea-tomcat100
Vendor:  cPanel, Inc.
Summary: EOL Tomcat
Version: 10.0.20
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 5
Release: %{release_prefix}%{?dist}.cpanel
License: Apache License, 2.0
Group:   System Environment/Daemons
URL: https://tomcat.apache.org/tomcat-10.0-eol.html

Source0: https://www-us.apache.org/dist/tomcat/tomcat-8/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1: ea-podman-local-dir-setup
Source2: README.md
Source3: test.jsp
Source4: pkg.prerm

# if I do not have autoreq=0, rpm build will recognize that the ea_
# scripts need perl and some Cpanel pm's to be on the disk.
# unfortunately they cannot be satisfied via the requires: tags.
Autoreq: 0

Requires: ea-apache24-mod_proxy_ajp
Requires: ea-podman

%description
Tomcat 10.0 has reached End of Life.

Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%prep
%setup -qn apache-tomcat-%{version}

%build
# empty build section

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100
cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/ea-podman-local-dir-setup
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.md
cp %{SOURCE3} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/test.jsp
echo -n "%{version}-%{release_prefix}" > $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/pkg-version

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/user-conf
cp -r ./conf/* $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/user-conf

cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/ea-podman-local-dir-setup
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/README.md
cp %{SOURCE3} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/test.jsp

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/bin

cat << EOF > $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat100/ea-podman.json
{
    "ports" : [8080, 8009],
    "image" : "docker.io/library/tomcat:%{version}",
    "startup" : {
        "-e" : ["CATALINA_OPTS=-Xmx100m", "CATALINA_BASE=/usr/local/tomcat"],
        "-v" : [
            "conf:/usr/local/tomcat/conf",
            "logs:/usr/local/tomcat/logs",
            "webapps:/usr/local/tomcat/webapps"
        ]
    }
}
EOF

%preun

%include %{SOURCE4}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/cpanel/ea-tomcat100
%attr(0655,root,root) /opt/cpanel/ea-tomcat100
%attr(0755,root,root) /opt/cpanel/ea-tomcat100/ea-podman-local-dir-setup
%attr(0644,root,root) /opt/cpanel/ea-tomcat100/ea-podman.json
%attr(0644,root,root) /opt/cpanel/ea-tomcat100/README.md
%attr(0644,root,root) /opt/cpanel/ea-tomcat100/test.jsp
%attr(0644,root,root) /opt/cpanel/ea-tomcat100/pkg-version

%changelog
* Mon May 05 2025 Dan Muey <daniel.muey@webpros.com> - 10.0.20-5
- ZC-12813: Add Almalinux_10 to DISABLE_BUILD in Makefile

* Wed Aug 02 2023 Julian Brown <julian.brown@cpanel.net> - 10.0.20-4
- ZC-11053: Mark as EOL

* Tue Jun 20 2023 Dan Muey <dan@cpanel.net> - 10.0.20-3
- ZC-11022: Add deployment info to user readme

* Tue May 09 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 10.0.20-2
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Tue May 10 2022 Dan Muey <dan@cpanel.net> - 10.0.20-1
- EA-10698: Update ea-tomcat100 from v10.0.14 to v10.0.20

* Thu Mar 31 2022 Dan Muey <dan@cpanel.net> - 10.0.14-3
- ZC-9892: Correct default `deployOnStartup`, Set `unpackWARs` to false initially

* Tue Feb 08 2022 Dan Muey <dan@pcanel.net> - 10.0.14-2
- ZC-9724: clean out tomcat 8.5/EA3 cruft and some fixes

* Fri Jan 14 2022 Julian Brown <julian.brown@webpros.com> - 10.0.14-1
- ZC-9647: Initial Build of tomcat 10.0 using podman

