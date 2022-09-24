# Linux Agent Plugin for CheckMK - TL-SG108E

 TL-SG108E is an "easy managed" network switch, as such - it does not support SSH/telnet or SNMP.
 This plugin piggyback the HOST stat on top the Linux Agent payload.
 
 * `agent_based` should be located in `/omd/sites/MONITORING_SITE/local/lib/check_mk/base/plugins/agent_based`
 * `agent_plugin` should be located in `/usr/lib/check_mk_agent/plugins` on the Agent host
 
 in `agent_plugin`->`tp_link.sh` modify the following:
 * `HOSTNAME` - switch HOSTNAME as defined in CheckMK
 * `SWITCH_IP` - switch local IP
 * `USERNAME` - TL-SG108E username
 * `PASSWORD` - TL-SG108E password
 
 Each port will be discovered as a service on the switch remote host
 
See https://docs.checkmk.com/latest/en/devel_check_plugins.html for more details
