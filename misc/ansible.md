
# Ansible

## Inventory file / hosts / hosts.yml

```
[cumulus]
cumulus ansible_ssh_host=10.255.0.10
cumulus ansible_ssh_port=22
cumulus ansible_ssh_user=cumulus
cumulus ansible_ssh_pass=CumulusLinux!
cumulus ansible_sudo_pass=CumulusLinux!
cumulus ansible_ssh_private_key_file=~/.ssh/id_rsa

[all:vars]
[cumulus:vars]
```

## Playbook

[user create](https://docs.ansible.com/ansible/latest/modules/user_module.html)
```
- user:
    name: stack
    password: "{{ 'stack' | password_hash('sha512') }}"
    shell: /usr/bin/bash
    home: /opt/stack
    state: present
```

[create file or directory (file module)](https://docs.ansible.com/ansible/latest/modules/file_module.html)
```
- file:
    path: /opt/stack/.ssh
    state: directory
    owner: stack
    group: stack
    mode: 755
```

shell
```
- shell: |
    echo slankdev > /tmp/out
    echo slankdev1 > /tmp/out2
    echo slankdev2 >> /tmp/out
```

file copy and fetch
```
- copy:
    src: files/bashrc
    dest: /etc/bashrc
    mode: 644
    owner: stack
    group: stack

- fetch:
    src: /tmp/filename
    dest: outputs
    # ./outputs/{{ hostname }}/tmp/filename

- fetch:
    src: /tmp/filename
    dest: outputs
    flat: yes
    # ./outputs/filename
```

yum install
```
- yum:
  name: {{ item }}
  state=present
  become: True
  with_items:
    - epel-release
    - e2fsprogs

- yum:
    name: /tmp/package.el7.x86_64.rpm
    state: present
```

execute on localhost
```
- hosts: localhost
  connection: local
  tasks:
    - ping:
```

tags
```
$ cat main.yml
---
- hosts: ws
  tasks:
    - shell: "echo slank1"
    - shell: "echo slank2"
      tags: red

$ ansible-playbook main.yml --tags='red'          #-->slank2
$ ansible-playbook main.yml --skip-tags='red'     #-->slank1
```

## Global Vars

```
  ansible_date_time.iso8601_basic_short
```

special vars
```yaml
all:
  children:
    robot:
      hosts:
        robot1:
        robot2
```

```yaml
{{ inventory_hostname }} # robot1,robot2
```

## nclu plugin for cumulus


```
- name: Remove IP address from interface swp1
  nclu:
    atomic: true
    description: "Ansible - add swp1"
    commands:
        - del int swp1 ip address 1.1.1.1/24

- name: Remove IP address from interface swp1
  nclu:
    commit: true
    commands:
        - del int swp1 ip address 1.1.1.1/24

- name: Add 48 interfaces and commit the change.
  nclu:
    template: |
        {% for iface in range(1,49) %}
        add int swp{{iface}}
        {% endfor %}
```

## Vault

ansible-vault で文字列を暗号化する時は, 以下のようにやるとミスるので.
```
echo 'PASSWORD' | ansible-vault encrypt_string
echo -n 'PASSWORD' | ansible-vault encrypt_string
```

以下のようにやるとよい.
```
ansible-vault encrypt_string 'PASSWORD' --name 'name_is_here'
```

special thanks: Kento.kawakami -san

## References

- @tmurakam99, "Ansible でよく使うモジュールまとめ",
  ここからたくさんwikiにかけることがある.
  https://qiita.com/tmurakam99/items/8e609f174f5804308a20

