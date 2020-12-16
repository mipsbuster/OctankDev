#!/usr/bin/env python3

from aws_cdk import core

from octank_dev.octank_dev_stack import OctankDevStack


app = core.App()
OctankDevStack(app, "octank-dev")

app.synth()
