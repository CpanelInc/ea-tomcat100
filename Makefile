OBS_PROJECT := EA4
OBS_PACKAGE := ea-tomcat100
DISABLE_BUILD := arch=i586 repository=Almalinux_10 repository=CentOS_6.5_standard repository=CentOS_7
include $(EATOOLS_BUILD_DIR)obs.mk
