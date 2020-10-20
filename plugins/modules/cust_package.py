#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2020 Abderrahmane Boulahdour, Inc. All Rights Reserved.

DOCUMENTATION = '''
module: cust_package
author: Abderrahmane Boulahdour (https://github.com/Arboulahdour)
description: This module allows to install or remove packages on debian-based linux distribution.

options:
  update: 
    description: This allows to update the system before the installation.
    required: no
    type: bool
  upgrade: 
    description: This allows to upgrade the system packages.
    required: no
    type: bool
  repository: 
    description: This refers to the name of the repository you should install before installing the package.
    required: no
    type: str   
  package: 
    description: This refers to the name of the package (e.g nginx, apache2, mysql etc..).
    required: yes
    type: str
  version:
    description: This refers to the version of the package.
    required: no
    type: str
  action: 
    description: This refers to the action (install or remove the package with all its dependencies) that you would apply against the package. 
    required: yes
    type: str 
 
'''

EXAMPLES = '''
- name: "installing nginx package" 
  arboulahdour.deb.cust_package:
    update: True  
    package: "nginx" 
    action: "install"

- name: "installing apache2:2.4.29-1ubuntu4.14 package"
  arboulahdour.deb.cust_package:
    update: True
    upgrade: True
    package: "{{ item }}"
    version: "2.4.29-1ubuntu4.14"
    action: "install"
    with_items:
     - apache

- name: "installing ansible package"
  arboulahdour.deb.cust_package:
    update: True
    upgrade: False
    repository: "ppa:ansible/ansible"
    package: "ansible"
    action: "install"

- name: "removing bind9 package" 
  arboulahdour.deb.cust_package:  
    package: "bind9" 
    action: "remove" 

'''

RETURN = '''
results: 
    description: returns the result of the execution (installation or deletion of package). 
'''

import os,subprocess,sys
from subprocess import PIPE, call, Popen

def main():

	fields = {
		"update": {"required": False, "type": "bool"},
		"upgrade": {"required": False, "type": "bool"},
		"repository": {"required": False, "type": "str"},
		"package": {"required": True, "type": "str"},
		"version": {
			"default": "latest",
			"required": False, 
			"type": "str"},
        "action": {
        	"required": True,
            "choices": ['install', 'remove'],
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

	if  module.params.get("update") is True:
		update = ["apt-get", "update"]
		rc = module.run_command(update, check_rc=True)
		message = "The system is updated & "

	if  module.params.get("upgrade") is True:
		upgrade = ["apt-get", "upgrade", "-y"]
		rc = module.run_command(upgrade, check_rc=True)
		message = "upgrade is done, "

	if  module.params.get("repository"):
		repository = str(module.params.get("repository")).strip()
		update = ["add-apt-repository", repository, "-y"]
		rc = module.run_command(update, check_rc=True)
		message = message + repository + " repository is added, "

	package = str(module.params.get("package")).strip()

	devnull = open(os.devnull,"w")
	retval = subprocess.call(["dpkg","-s",package],stdout=devnull,stderr=subprocess.STDOUT)
	devnull.close()

	version = str(module.params.get("version"))

	if module.params.get("action") == "install":
	
		if version == "latest":
			if retval != 0:
				action = module.params.get("action")
				install_pkg = ["apt-get", action , package, "-y"]
				rc = module.run_command(install_pkg, check_rc=True)

				if rc[0] != 0:
					module.fail_json(msg='unable to install package (result returned non-0). Please, try again.')
				
				message = message + package + ":" + version + " package has been successfully installed"
				result['changed'] = True
				module.exit_json(changed=True, meta=message)
			
			else:
				message = message + package + ":" + version + " package is installed"
				result['changed'] = False
				module.exit_json(changed=False, meta=message)

		else:
			if retval != 0:
				action = module.params.get("action")
				pkvers = package + "=" + version
				install_pkg = ["apt-get", action, pkvers,"-y"]
				rc = module.run_command(install_pkg, check_rc=True)

				if rc[0] != 0:
					module.fail_json(msg='unable to install package (result returned non-0). Please, try again.')
				
				message = message + package + ":" + version + " package has been successfully installed"
				result['changed'] = True
				module.exit_json(changed=True, meta=message)
			
			else:
				ps = subprocess.Popen(('dpkg', '-s', package), stdout=subprocess.PIPE)
				check_vers = subprocess.check_output(('grep', version), stdin=ps.stdout)
				ps.wait()
				get_vers = check_vers.split()
				if get_vers[1] == version:
					message = message + package + ":" + version + " package is installed"
					result['changed'] = False
					module.exit_json(changed=False, meta=message)
				else:
					action = module.params.get("action")
					remove_pkg = ["apt-get", "remove" , package, "-y"]
					rc = module.run_command(remove_pkg, check_rc=True)

					if rc[0] != 0:
						module.fail_json(msg='unable to remove package (result returned non-0). Please, try again.')
					
					purge_pkg = ["apt-get", "purge", package, "-y"]
					rc_au = module.run_command(purge_pkg, check_rc=True)

					if rc_au[0] != 0:
						module.fail_json(msg='unable to remove package (result returned non-0). Please, try again.')
					action = module.params.get("action")
					pkvers = package + "=" + version
					install_pkg = ["apt-get", action , pkvers,"-y"]
					rc = module.run_command(install_pkg, check_rc=True)

					if rc[0] != 0:
						module.fail_json(msg='unable to install package (result returned non-0). Please, try again.')
				
					message = message + package + ":" + version + " package has been successfully installed"
					result['changed'] = True
					module.exit_json(changed=True, meta=message)

	else:

		if retval != 0:
			message = message + package + ":" + version + " package is not installed"
			result['changed'] = False
			module.exit_json(changed=False, meta=message)
			
		else:
			action = module.params.get("action")
			remove_pkg = ["apt-get", action , package, "-y"]
			rc = module.run_command(remove_pkg, check_rc=True)

			if rc[0] != 0:
				module.fail_json(msg='unable to remove package (result returned non-0). Please, try again.')
			
			purge_pkg = ["apt-get", "purge", package, "-y"]
			rc_au = module.run_command(purge_pkg, check_rc=True)

			if rc_au[0] != 0:
				module.fail_json(msg='unable to remove package (result returned non-0). Please, try again.')
				
			message = message + package + ":" + version + " package has been successfully removed."
			result['changed'] = True
			module.exit_json(changed=True, meta=message)
		

	
		
if __name__ == '__main__':

	from ansible.module_utils.basic import *
	main()