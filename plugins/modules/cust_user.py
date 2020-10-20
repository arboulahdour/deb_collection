#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2020 Abderrahmane Boulahdour, Inc. All Rights Reserved.

DOCUMENTATION = '''
module: cust_user
author: Abderrahmane Boulahdour (https://github.com/Arboulahdour)
description: This module allows to create or delete users on debian-based linux distribution.

options: 
  name: 
    description: This refers to the name of the user.
    required: yes
    type: str
  uid:
    description: This refers to the process ID of the user.
    required: no
    type: int
  group:
    description: This refers to the primary group of the created user.
    required: no
    type: str
  password:
    description: This refers to the password of the user.
    required: no
    type: str
  groups:
    description: This refers to the list of the groups user will be added to.
    required: no
    type: str
  shell:
    description: This sets the user's shell.
    required: no
    type: str
  create_dir:
    description: This sets the user's home directory.
    required: no
    type: str
  comment:
    description: This  sets the description of user account.
    required: no
    type: str
  state: 
    description: This refers to the state (present or absent) that you would apply against the user. 
    required: yes
    type: str 
 
'''

EXAMPLES = '''
- name: "creating user named netadmin" 
  arboulahdour.deb.cust_user:
    name: "netadmin"
    state: "present"

- name: "creating user named admin with uid 1500"
  arboulahdour.deb.cust_user:
    name: "admin"
    uid: 1500
    state: "present"

- name: "creating user named admin with an encrypted password"
  arboulahdour.deb.cust_user:
    name: "admin"
    password: "$1$admin$901hj85myhfpGsr2aYoAi5n"
    state: "present"

- name: "creating user named admin with its home directory"
  arboulahdour.deb.cust_user:
    name: "admin"
    create_dir: True
    state: "present"    

- name: "removing user named user2" 
  arboulahdour.deb.cust_user:
    name: "user2"
    state: "absent"

- name: "creating user named user1" 
  arboulahdour.deb.cust_user:
    name: "{{ item }}"
    uid: 2000
    group: "root"
    password: "$1$user1$./1GL88mvkhpGsr2aYOpW1"
    groups: "root"
    shell: "/bin/bash"
    create_dir: True
    comment: "Hello from user1!"
    state: "present"
   with_items:
    - user1

'''

RETURN = '''
results: 
    description: returns the result of the execution (creation or deletion of user). 
'''

import os,subprocess,sys
from subprocess import call

def main():

	fields = {
		"name": {"required": True, "type": "str"},
		"uid": {"required": False, "type": "int"},
		"group": {"required": False, "type": "str"},
		"password": {"required": False, "type": "str", "no_log": True},
		"groups": {"required": False, "type": "str"},
		"shell": {"required": False, "type": "str"},
		"create_dir": {"required": False, "default": False, "type": "bool"},
		"comment": {"required": False, "type": "str"},
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

	user = str(module.params.get("name")).strip()

	uid = module.params.get("uid")
	group = module.params.get("group")
	password = module.params.get("password")
	groups = module.params.get("groups")
	shell = module.params.get("shell")
	create_dir = module.params.get("create_dir")
	comment = module.params.get("comment")

	check_usr = call(["egrep", "-w", user, "/etc/passwd"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if module.params.get("state") == "present":

			create_usr = [user]

			if uid is None:
				create_usr = create_usr
			else:
				create_usr = create_usr + ["-u", str(uid)]

			if group is None:
				create_usr = create_usr
			else:
				create_usr = create_usr + ["-g", str(group)]

			if password is None:
				create_usr = create_usr
			else:
				create_usr = create_usr + ["-p", str(password)]

			if groups is None:
				create_usr = create_usr
			else:
				create_usr = create_usr + ["-G", str(groups)]

			if shell is None:
				create_usr = create_usr
			else:
				create_usr = create_usr + ["-s", str(shell)]

			if create_dir is True:
				create_usr = create_usr + ["-m"]
			else:
				create_usr = create_usr

			if comment is None:
				create_usr = create_usr
			else:
				create_usr = create_usr + ["-c", str(comment)] 
			
			if check_usr != 0:

				create_usr = ["useradd"] + create_usr 
				rc = module.run_command(create_usr, check_rc=True)

				if rc[0] != 0:
					module.fail_json(msg='unable to create user (result returned non-0). Please, try again.')
				
				message = user + " user has been successfully created"
				result['changed'] = True
				module.exit_json(changed=True, msg=message)
			
			else:
				message = user + " user exists."
				result['changed'] = False
				module.exit_json(changed=False, msg=message)

	else:

		if check_usr != 0:
			message = user + " user is not created"
			result['changed'] = False
			module.exit_json(changed=False, msg=message)
			
		else:
			remove_usr = ["userdel", user]
			rc = module.run_command(remove_usr, check_rc=True)

			if rc[0] != 0:
				module.fail_json(msg='unable to delete user (result returned non-0). Please, try again.')

			direc = " /home/" + user
			remove_dir = "rm -r" + direc
			os.system(remove_dir)	
			message = user + " user has been successfully removed."
			
			result['changed'] = True
			module.exit_json(changed=True, msg=message)
				
		
if __name__ == '__main__':

	from ansible.module_utils.basic import *
	main()