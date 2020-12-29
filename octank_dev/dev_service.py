from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_ec2 as ec2,
                     aws_rds as rds,
                     aws_cloudwatch as cloudwatch,
                     aws_lambda as lambda_)
from aws_cdk.core import CfnParameter

class DevService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        vpc = ec2.Vpc(self, "VPC-Octank-DEV")

        bucket = s3.Bucket(self, "DevStore")

        handler = lambda_.Function(self, "DevHandler",
                    runtime=lambda_.Runtime.NODEJS_10_X,
                    code=lambda_.Code.asset("resources"),
                    handler="dev.main",
                    environment=dict(
                    BUCKET=bucket.bucket_name)
                    )

        bucket.grant_read_write(handler)

        api = apigateway.RestApi(self, "dev-api",
                  rest_api_name="Dev Service",
                  description="This service serves dev.")

        get_devs_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_devs_integration)   # GET /

        dev = api.root.add_resource("{id}")

        # Add new dev to bucket with: POST /{id}
        post_dev_integration = apigateway.LambdaIntegration(handler)

        # Get a specific dev from bucket with: GET /{id}
        get_dev_integration = apigateway.LambdaIntegration(handler)

        # Remove a specific dev from the bucket with: DELETE /{id}
        delete_dev_integration = apigateway.LambdaIntegration(handler)

        dev.add_method("POST", post_dev_integration);  # POST /{id}
        dev.add_method("GET", get_dev_integration);  # GET /{id}
        dev.add_method("DELETE", delete_dev_integration);  # DELETE /{id}
#        engine = rds.DatabaseInstanceEngine.postgres(
 #           version=rds.PostgresEngineVersion.VER_12_4 engine=rds.DatabaseClusterEngine.AURORA_POSTGRESQL,

        custom_engine_version = rds.AuroraMysqlEngineVersion.of("5.7.mysql_aurora.2.08.1")

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        cluster = rds.DatabaseCluster(self, "Database",
                                      engine=rds.DatabaseClusterEngine.aurora_postgres(
                                          version=rds.AuroraPostgresEngineVersion.VER_11_8 ),
                                      credentials=rds.Credentials.from_generated_secret("clusteradmin"),
                                      # Optional - will default to 'admin' username and generated password
                                      instance_props={
                                          # optional , defaults to t3.medium
                                          "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                                                               ec2.InstanceSize.SMALL),
                                          "vpc_subnets": {
                                              "subnet_type": ec2.SubnetType.PRIVATE
                                          },
                                          "vpc": vpc
                                      }
                                      )

        metricCPU = cluster.metric_cpu_utilization()
        alarmCPU = cloudwatch.Alarm(self, "AlarmCPU",
                                 metric=metricCPU,
                                 threshold=75,
                                 evaluation_periods=3,
                                 datapoints_to_alarm=2
                                 )


        #metric = rds.metric("HighBilledVolumeBytesUsed")
"""        rdsDev = rds.DatabaseInstance(
            self, "database-dev01",
            database_name="db1",
            engine=rds.ServerlessCluster(self,"devServerless",engine=IClusterEngine,vpc=vpc,
                                         default_database_name='devServerless'
            ),
            vpc=vpc,
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,allow_major_version_upgrade=True,
            auto_minor_version_upgrade=True,copy_tags_to_snapshot=True
        )
"""