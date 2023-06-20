# ea-tomcat100 EA4 container based package

## Security

Please read https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html
to find ways to increase security of your tomcat instance.

## Faster Startup

Please read https://wiki.apache.org/tomcat/HowTo/FasterStartUp
to find ways to improve the startup time fo your tomcat instance.

## Test Script

`/opt/cpanel/ea-tomcat100/test.jsp` is a handy JSP test script that you can copy to try out your instance.

See _How do I deploy my code?_ to learn about deployment.

## How do I deploy my code?

There are various ways to deploy your code, each with its own security implications. The method that you use will depend on your needs and circumstances. Our default configuration is designed to allow you to make informed choices and pick the best method for your use case.

To determine which method is the best for you, read [Tomcat’s Security](https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html) documentation. Then, read the [Tomcat Web Application Deployment](https://tomcat.apache.org/tomcat-10.1-doc/deployer-howto.html) documentation to choose the method you wish to use.

## How do I start/stop/etc my container?

It is managed by the `ea-podman` system.

`/usr/local/cpanel/scripts/ea-podman hint` to get started.

## I want to access my apps via URI and not need a port number

You simply need to configure your web server to proxy a given URI to the appropriate port.

For example:

* given an AJP port of `11111`
* assuming you want `example.com/testuri` to serve the test.jsp noted above

You’d need to:

1. create a `ProxyPass` include for Apache.
   * An [include for `example.com`](https://docs.cpanel.net/ea4/apache/modify-apache-virtual-hosts-with-include-files/) would look like this:
```
<IfModule proxy_ajp_module>
    ProxyPass "/testuri" "ajp://127.0.0.1:11111/test.jsp"
</IfModule>
```
2. restart apache
3. Hit example.com/testuri to ensure it took effect

**Note**: The ajp module in that example is brought in as a requirement of `ea-tomcat100`.
