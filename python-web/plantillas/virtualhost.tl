<VirtualHost *:80>
    ServerName www.&dom&
    ServerAlias &dom&
 
    DocumentRoot /var/www/&dom&/
 
    ServerSignature On
 
    ErrorLog /var/log/apache2/nom&dom&-error.log
 
    LogLevel warn
 
    CustomLog /var/log/apache2/dominio.com-access.log combined
 
    <Directory "/var/www/&dom&/">
    Options Indexes FollowSymLinks MultiViews ExecCGI
        AllowOverride All
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
