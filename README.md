deb collection
==============

Here in this collection you will find some customs ansible modules developed using python to interact with your local machine, an API, or a remote system to perform specific tasks like installing packages and services, changing the state of an installed service on linux operating systems, running specifics commands or configuring users and groups on the servers.

Requirements
------------

Debian-based linux distribution.
python 2.x installed.


Example Playbook
----------------

    - name: "NGINX" 
  	  arboulahdour.deb.cust_service:
        service: "nginx"
        state: "started"

    - name: "BIND9" 
  	  arboulahdour.deb.cust_service:
        service: "bind9"
        state: "stopped"
 
    - name: Installing apache2:2.4.29-1ubuntu4.14 package
      arboulahdour.deb.cust_package:
        update: True
        package: "{{ item }}"
        version: "2.4.29-1ubuntu4.14"
        action: "install"
      with_items:
       - apache2

    - name: Installing ansible package
      arboulahdour.deb.cust_package:
        update: True
        repository: "ppa:ansible/ansible"
        package: "ansible"
        action: "install"

    - name: Creating group named management_grp 
      arboulahdour.deb.cust_group:
        name: "management_grp" 
        state: "present"

    - name: Removing nginx package
      arboulahdour.deb.cust_package:
        package: "nginx"
        action: "remove"

    - name: Creating group named admin with gid 2000
      arboulahdour.deb.cust_group:
        name: "admin"
        gid: 2000 
        state: "present"

    - name: Removing group named test_grp 
      arboulahdour.deb.cust_group:  
        name: "test_grp" 
        state: "absent"

    - name: "creating user named admin" 
      arboulahdour.deb.cust_user:
        name: "admin"
        uid: 1500
        group: "admin"
        password: "$1$admin$./1GL88mvkhpGsr2aYOpW1"
        groups: "root"
        shell: "/bin/bash"
        create_dir: True
        comment: "Hello from admin!"
        state: "present"

Author Information
------------------

Author: Abderrahmane Boulahdour;
LinkedIn: https://www.linkedin.com/in/abderrahmane-boulahdour-462165169;
Github: https://github.com/Arboulahdour;
Twitter: https://twitter.com/ABoulahdour;
Portfolio: https://arboulahdour.github.io/portfolio;
personal website: https://arboulahdour.github.io/info
