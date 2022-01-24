. /opt/cpanel/ea-podman/ea-podman.sh
. /opt/cpanel/ea-tomcat100/bin/user-functions
. $HOME/ea-tomcat100/bin/setenv.sh

ERROR=0
case $1 in
    start)
        name=`get_user_container_name "ea_tomcat100"`
        $(is_container_name_running $name)
        ret=$?
        if [ $ret -eq 0 ]; then
            echo -e "\e[00;33Tomcat 10.0 container is already running (name : $name)\e[00m"
            ERROR=1
        else
            /opt/cpanel/ea-tomcat100/bin/user-startup.sh
        fi
        ;;
    stop)
        name=`get_user_container_name "ea_tomcat100"`
        $(is_container_name_running $name)
        ret=$?
        if [ $ret -gt 1 ]; then
            echo -e "\e[00;31mTomcat 10.0 container is already shutdown\e[00m"
            ERROR=1
        else
            /opt/cpanel/ea-tomcat100/bin/user-shutdown.sh
        fi
        ;;
    restart|force-reload|reload)
        name=`get_user_container_name "ea_tomcat100"`
        $(is_container_name_running $name)
        ret=$?
        if [ $ret -eq 0 ]; then
            /opt/cpanel/ea-tomcat100/bin/user-shutdown.sh
        fi

        /opt/cpanel/ea-tomcat100/bin/user-startup.sh
        ;;
    status|fullstatus)
        name=`get_user_container_name "ea_tomcat100"`
        $(is_container_name_running $name)
        ret=$?
        if [ $ret -gt 0 ]; then
            echo -e "\e[00;31mTomcat 10.0 is currently not running.\e[00m"
            ERROR=3
        else
           echo -e "\e[00;32mTomcat 10.0 is running!\e[00m"
           ERROR=0
        fi  
        ;;  
    realstatus)
        num_tomcat=`ps l -u $USER | grep java | grep tomcat | wc -l`
        if [ $num_tomcat -eq 0 ]; then
            echo -e "\e[00;31mTomcat 10.0 is currently not running.\e[00m"
            ERROR=3
        else
           echo -e "\e[00;32mTomcat 10.0 is running!\e[00m"
           ERROR=0
        fi
        ;;
    *)  
        echo $"Usage: $0 {start|stop|restart|status|fullstatus}"
        ERROR=2
        ;;  
esac
 
exit $ERROR
