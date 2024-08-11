import aws_cdk as core
import aws_cdk.assertions as assertions

from cdkpython_sso.cdkpython_sso_stack import CdkpythonSsoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdkpython_sso/cdkpython_sso_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkpythonSsoStack(app, "cdkpython-sso")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
