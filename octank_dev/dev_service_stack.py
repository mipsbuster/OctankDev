from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core,
)
from aws_cdk.core import CfnParameter
from dev_service import DevService

class MyDevServiceStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        cust_id = CfnParameter(self, "custId", type="String",
                                          description="The id of the customer.")
        #cust_name = CfnParameter(self, "custName", type='String', description="The name of the customer.")
        #group_id = CfnParameter(self, "groupId", type="String", description="The id of the group.")
        '''product_id = CfnParameter(self, "prodId", type="String",
                                          description="The id of the prod.")
'''
        core.Tags.of(self).add("customer-ID", cust_id.value_as_string,priority=100)
        #core.Tags.of(self).add("group-ID", "beta-dev-team")
        #core.Tags.of(self).add("customer-Name", "Jon-george")


        DevService(self, "DevService")


        print(cust_id.value_as_string)





