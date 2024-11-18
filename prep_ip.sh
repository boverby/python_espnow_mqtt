#!/bin/bash -x


# modified from https://github.com/ChuckMash/ESPythoNOW/prep.sh

#  defaults or parameters condif
INTERFACE="${1:-"wlp1s0"}"
CHANNEL="${2:-"1"}"


#    debian host for wireless gateway:
# Network:   Device-1: Realtek RTL8821AE 802.11ac PCIe Wireless Network Adapter driver: rtl8821ae v: kernel port: e000
#            bus ID: 01:00.0 chip ID: 10ec:8821 class ID: 0280
#            IF: wlp1s0 state: down mac: b0:c0:90:09:0f:ed

#(espnow) root@beebox:/ iwconfig wlp1s0
# wlp1s0    IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=20 dBm
#           Retry short limit:7   RTS thr=2347 B   Fragment thr:off
#           Power Management:on
#  frequency  available:
#        * 2412 MHz [1] (22.0 dBm)
#        * 2417 MHz [2] (22.0 dBm)
#        * 2422 MHz [3] (22.0 dBm)
#        * 2427 MHz [4] (22.0 dBm)
#        * 2432 MHz [5] (22.0 dBm)
#        * 2437 MHz [6] (22.0 dBm)
#        * 2442 MHz [7] (22.0 dBm)
#        * 2447 MHz [8] (22.0 dBm)
#        * 2452 MHz [9] (22.0 dBm)
#        * 2457 MHz [10] (22.0 dBm)
#        * 2462 MHz [11] (22.0 dBm)
#        * 2467 MHz [12] (22.0 dBm)
#        * 2472 MHz [13] (22.0 dBm)
#        * 2484 MHz [14] (disabled)

ip link set ${INTERFACE} down
iw dev ${INTERFACE} set monitor none
iw dev ${INTERFACE} set type monitor
ip link set ${INTERFACE} up
iw dev ${INTERFACE} set freq 2412
