#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2020 Abderrahmane Boulahdour, Inc. All Rights Reserved.

DOCUMENTATION = '''
module: cust_service
author: Abderrahmane Boulahdour (https://github.com/Arboulahdour)
description: This module allows to start, restart or stop services on debian-based linux distribution..

options: 
  service: 
    description: This refers to the name of the service (e.g nginx, apache, mysql etc..).
    required: yes
    type: str 
  state: 
    description: This refers to the state (started, stopped or restarted) that you would apply to the service. 
    required: yes
    type: str 
 
'''

EXAMPLES = '''
- name: "NGINX" 
  arboulahdour.deb.cust_service:  
    service: "nginx" 
    state: "started"

- name: "APACHE2" 
  arboulahdour.deb.cust_service:  
    service: "apache2" 
    state: "stopped" 
'''

RETURN = '''
results: 
    description: returns the result of the execution (the new state of the service) 
'''

import os,subprocess,sys

def main():

	fields = {
		"service": {"required": True, "type": "str"},
        "state": {
        	"required": True,
            "choices": ['started', 'stopped', 'restarted'],
            "type": 'str'
        },
	}
	
	module = AnsibleModule(
		argument_spec=fields,
		supports_check_mode=True
	)

	service = str(module.params.get("service")).strip()
	p =  subprocess.Popen(["systemctl", "is-active",  service], stdout=subprocess.PIPE)
	(state, err) = p.communicate()
	state = state.decode('utf-8')

	result = dict(
		changed=False,
	)

	if module.check_mode:
		module.exit_json(**result)


	cmd = "service"

	state = str(state).strip()

	if module.params.get("state") == "started":
	
		if state == "inactive":

			run = [cmd, service, 'start']
			rc = module.run_command(run, check_rc=True)

			if rc[0] != 0:
				module.fail_json(msg='unable to run command (result returned non-0)')
			
			result['changed'] = True
			module.exit_json(changed=True, meta="process state has been changed from inactive to active")
			

		else:
				
			result['changed'] = False
			module.exit_json(changed=False, meta="process state has not been changed (active)")

	elif module.params.get("state") == "stopped":

		if state == "active":

			run = [cmd, service, 'stop']
			rc = module.run_command(run, check_rc=True)

			if rc[0] != 0:
				module.fail_json(msg='unable to run command (result returned non-0)')
			
			result['changed'] = True
			module.exit_json(changed=True, meta="process state has been changed from active to inactive")
			

		else:
				
			result['changed'] = False
			module.exit_json(changed=False, meta="process state has not been changed (inactive)")

	else:

		run = [cmd, service, 'restart']
		rc = module.run_command(run, check_rc=True)

		if rc[0] != 0:
			module.fail_json(msg='unable to run command (result returned non-0)')
		
		result['changed'] = True
		module.exit_json(changed=True, meta="process state has been restarted")

		
if __name__ == '__main__':

	from ansible.module_utils.basic import *
	main()