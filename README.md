# igate_monitor
View received packets from an iGate LoRa APRS in a Telegram Bot

Simple procedure written in Python3 that receives packets from a LoRa APRS iGate (**Kiss functionality must be enabled in the iGate**) by [CA2RXU](https://github.com/richonguzman/LoRa_APRS_iGate) and sends them to a Telegram Bot.<br><br>
**First step**

Create your Telegram Bot following BotFather's instructions inside Telegram. Start it and retrieve your CHAT ID, then insert your API TOKEN and CHAT ID into the igate_monitor.sh script. The .sh script must be runnable. You need curl present in your system to run the Bot. You can test if everything works by running **sh igate_monitor.sh TEXT** (needs an argument).<br><br>

**Second step**

Edit the python code and specify the TNC IP/DNS and port in the configuration section. Nothing else is needed. You can run the code and check that it reaches the TNC, then wait for your iGate LoRa to receive APRS packets from the network. These will be displayed and sent to the script that runs the Bot. The two files must reside in the same folder. If the iGate is restarted or becomes unreachable, you will need to restart the program. To put it in the background you can use this syntax: **nohup python3 igate_monitor.py &**<br><br>



