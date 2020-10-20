#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2020 Abderrahmane Boulahdour, Inc. All Rights Reserved.

DOCUMENTATION = '''
module: cust_group
author: Abderrahmane Boulahdour (https://github.com/Arboulahdour)
description: This module allows to create or delete groups on debian-based linux distribution.

options: 
  name: 
    description: This refers to the name of the group.
    required: yes
    type: str
  gid:
    description: This refers to the process ID of the group.
    required: no
    type: int
  state: 
    description: This refers to the state (present or absent) that you would apply against the group. 
    required: yes
    type: str 
 
'''

EXAMPLES = '''
- name: "creating group named management_grp" 
  arboulahdour.deb.cust_group:
    name: "management_grp"
    state: "present"

- name: "creating group named guest_grp with gid 2000"
  arboulahdour.deb.cust_group:
    name: "guest_grp"
    gid: 2000
    state: "present"

- name: "removing group named test_grp" 
  arboulahdour.deb.cust_group:
    name: "test_grp"
    state: "absent" 

'''

RETURN = '''
results: 
    description: returns the result of the execution (creation or deletion of group). 
'''

import os,subprocess,sys
from subprocess import call

def main():

	fields = {
		"name": {"required": True, "type": "str"},
		"gid": {"required": False, "type": "int"},
        "state": {
        	"required": True,
            "choices": ['present', 'absent'],
            "type": 'str'
        },
	}
	
	module = AnsibleModule(
		argument_spec=fields,
		supports_check_mode=True
	)

	result = dict(
		changed=False,
	)

	if module.check_mode:
		module.exit_json(**result)

	message = ""

	group = str(module.params.get("name")).strip()

	gid = module.params.get("gid")

	check_grp = call(["egrep", "-w", group, "/etc/group"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if module.params.get("state") == "present":
			
			if check_grp != 0:
				if gid is None:
					install_pkg = ["groupadd", group]
				else:
					install_pkg = ["groupadd", group, "-g", str(gid)]

				rc = module.run_command(install_pkg, check_rc=True)

				if rc[0] != 0:
					module.fail_json(msg='unable to create group (result returned non-0). Please, try again.')
				
				message = group + " group has been successfully created"
				result['changed'] = True
				module.exit_json(changed=True, msg=message)
			
			else:
				message = group + " group exists."
				result['changed'] = False
				module.exit_json(changed=False, msg=message)

	else:

		if check_grp != 0:
			message = group + " group is not created"
			result['changed'] = False
			module.exit_json(changed=False, msg=message)
			
		else:
			remove_pkg = ["groupdel", group]
			rc = module.run_command(remove_pkg, check_rc=True)

			if rc[0] != 0:
				module.fail_json(msg='unable to delete group (result returned non-0). Please, try again.')
			
			message = group + " group has been successfully removed."
			result['changed'] = True
			module.exit_json(changed=True, msg=message)
			
		
if __name__ == '__main__':

	from ansible.module_utils.basic import *
	main()