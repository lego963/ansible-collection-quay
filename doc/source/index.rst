=======================
Ansible-collection-guay
=======================

This collection helps to get info about quay tags using Ansible.


How to use it
-------------

.. code-block:: yaml

   ansible-playbook playbooks/run.yaml \
     -e repository=REPOSITORY \
     -e only_active_tags=true
