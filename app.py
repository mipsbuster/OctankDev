#!/usr/bin/env python3

from aws_cdk import core

from octank_dev.octank_dev_stack import OctankDevStack
from octank_dev import dev_service_stack

prod = core.Environment(account="610880146692", region="us-west-2")
app = core.App()
OctankDevStack(app, "octank-dev")
app.synth()
