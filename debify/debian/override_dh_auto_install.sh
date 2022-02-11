#!/bin/bash

source debian/vars.sh

mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100
cp -r ./* $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100
cp $SOURCE1 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/ea-podman-local-dir-setup
cp $SOURCE2 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/README.md
cp $SOURCE3 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/test.jsp
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/user-conf
cp -r ./conf/* $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/user-conf
cp $SOURCE1 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/ea-podman-local-dir-setup
cp $SOURCE2 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/README.md
cp $SOURCE3 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/test.jsp
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/bin
cat << EOF > ea-podman.json
{
    "ports" : [8080, 8009],
    "image" : "docker.io/library/tomcat:$version",
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
cp ea-podman.json $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat100/ea-podman.json
