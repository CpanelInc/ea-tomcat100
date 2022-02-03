# Your customizations can go here, for example, CATALINA_OPTS

# example from https://wiki.apache.org/tomcat/HowTo/FasterStartUp#Entropy_Source
# Trade some security for startup speed by using non-blocking entropy:
CATALINA_OPTS="$CATALINA_OPTS -Djava.security.egd=file:/dev/./urandom"
