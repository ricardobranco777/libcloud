from __future__ import with_statement

import os

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment

# Path to the public key you would like to install
KEY_PATH = os.path.expanduser("~/.ssh/id_rsa.pub")

# Shell script to run on the remote server
SCRIPT = """#!/usr/bin/env bash
apt-get -y update && apt-get -y install puppet
"""

RACKSPACE_USER = "your username"
RACKSPACE_KEY = "your key"

Driver = get_driver(Provider.RACKSPACE)
conn = Driver(RACKSPACE_USER, RACKSPACE_KEY)

with open(KEY_PATH) as fp:
    content = fp.read()

# Note: This key will be added to the authorized keys for the root user
# (/root/.ssh/authorized_keys)
step_1 = SSHKeyDeployment(content)

# A simple script to install puppet post boot, can be much more complicated.
step_2 = ScriptDeployment(SCRIPT)

msd = MultiStepDeployment([step_1, step_2])

images = conn.list_images()
sizes = conn.list_sizes()

# deploy_node takes the same base keyword arguments as create_node.
node = conn.deploy_node(name="test", image=images[0], size=sizes[0], deploy=msd)
