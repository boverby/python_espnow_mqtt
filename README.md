# python_espnow_mqtt


## combining code from :
>  https://github.com/ChuckMash/ESPythoNOW  - receives espnow packets with library ESPythoNOW.py
>  https://github.com/u-fire  - esp32  esphome based  client and bridge
>>       note : the esphome bridge from ufire was unreliable for me. Tried several 
>>              diff esp32, several brokers and dev boards and it always just timed 
>>              out after 1-2 publishes

## prep directory
```
  git clone https://github.com/ChuckMash/ESPythoNOW
  mkdir /opt/espnow
  cd /opt
  python -m venv  espnow
  cd /opt/espnow
  source  /opt/espnow/bin/activate
  cp [place_you_put_ESPythoNOW]/ESPythoNOW/ESPythoNOW.py /opt/espnow/

  pip3 install scapy
  pip3 install paho-mqtt
```
## creating test
```
edit python_espnow_mqtt.py for defaults for broker, port, prefix, wlan
modify interface and channel and run prep_ip.sh

  time to crete espnow messages form ufile compatible clients
  
```

## steps to add in systemd:

  create  /etc/systemd/system/python_espnow_mqtt.service

------------------- snip ------------------------------------
```
    [Unit]
    Description=python implementation of NOW_MQTT bridge
    After=network.target

    [Service]
    Environment=PYTHONUNBUFFERED=1
    Type=simple
#   ExecStart=/opt/espnow/bin/python3 /opt/espnow/python_espnow_mqtt.py
    ExecStart=/bin/bash -c 'cd /opt/espnow && source /opt/espnow/bin/activate && /opt/espnow/bin/python /opt/espnow/python_espnow_mqtt.py'
    WorkingDirectory=/opt/espnow
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target
```
------------------- snip ------------------------------------

## steps to manage in systemd:
* sudo systemctl daemon-reload
* sudo systemctl enable python_espnow_mqtt.service
* sudo systemctl start  python_espnow_mqtt.service
* sudo systemctl status python_espnow_mqtt.service
## steps to follow logs:
* sudo journalctl -u python_espnow_mqtt.service
* sudo journalctl  --since "1 min ago" -f -u python_espnow_mqtt.service



