import win32api
import win32con
import time


input('132321')
time.sleep(1)

win32api.keybd_event(0x0D, 0, 0, 0)
win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)


# <VirtualHost *:8000>
# #UWAMP Generate Virtual Host
# 	DocumentRoot "{DOCUMENTPATH}"
# 	ServerName "wagon"
# 	Alias "/mysql/" "{PHPAPPS}/adminer/"
# 	Alias "/mysql" "{PHPAPPS}/adminer/"
# 	Alias "/uwamp/" "{PHPAPPS}/uwamp/"
# 	Alias "/uwamp" "{PHPAPPS}/uwamp/"
# 	Alias "/adminer/" "{PHPAPPS}/adminer/"
# 	Alias "/adminer" "{PHPAPPS}/adminer/"
# 	<Directory "{PHPAPPS}/uwamp/">
# 		AllowOverride All
# 		Options FollowSymLinks Includes Indexes
#
# 	</Directory>
# 	<Directory "{PHPAPPS}/adminer/">
# 		AllowOverride All
# 		Options FollowSymLinks Includes Indexes
#
# 	</Directory>
# 	<Directory "{DOCUMENTPATH}/">
# 		AllowOverride All
# 		Options FollowSymLinks Indexes
# 		{ONLINE_MODE}
# 	</Directory>
# </VirtualHost>