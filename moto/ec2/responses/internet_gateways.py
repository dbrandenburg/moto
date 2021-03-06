from __future__ import unicode_literals
from moto.core.responses import BaseResponse
from moto.ec2.utils import (
    sequence_from_querystring,
    filters_from_querystring,
)


class InternetGateways(BaseResponse):
    def attach_internet_gateway(self):
        igw_id = self.querystring.get("InternetGatewayId", [None])[0]
        vpc_id = self.querystring.get("VpcId", [None])[0]
        self.ec2_backend.attach_internet_gateway(igw_id, vpc_id)
        template = self.response_template(ATTACH_INTERNET_GATEWAY_RESPONSE)
        return template.render()

    def create_internet_gateway(self):
        igw = self.ec2_backend.create_internet_gateway()
        template = self.response_template(CREATE_INTERNET_GATEWAY_RESPONSE)
        return template.render(internet_gateway=igw)

    def delete_internet_gateway(self):
        igw_id = self.querystring.get("InternetGatewayId", [None])[0]
        self.ec2_backend.delete_internet_gateway(igw_id)
        template = self.response_template(DELETE_INTERNET_GATEWAY_RESPONSE)
        return template.render()

    def describe_internet_gateways(self):
        filter_dict = filters_from_querystring(self.querystring)
        if "InternetGatewayId.1" in self.querystring:
            igw_ids = sequence_from_querystring(
                "InternetGatewayId", self.querystring)
            igws = self.ec2_backend.describe_internet_gateways(igw_ids, filters=filter_dict)
        else:
            igws = self.ec2_backend.describe_internet_gateways(filters=filter_dict)

        template = self.response_template(DESCRIBE_INTERNET_GATEWAYS_RESPONSE)
        return template.render(internet_gateways=igws)

    def detach_internet_gateway(self):
        # TODO validate no instances with EIPs in VPC before detaching
        # raise else DependencyViolationError()
        igw_id = self.querystring.get("InternetGatewayId", [None])[0]
        vpc_id = self.querystring.get("VpcId", [None])[0]
        self.ec2_backend.detach_internet_gateway(igw_id, vpc_id)
        template = self.response_template(DETACH_INTERNET_GATEWAY_RESPONSE)
        return template.render()


ATTACH_INTERNET_GATEWAY_RESPONSE = u"""<AttachInternetGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2013-10-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <return>true</return>
</AttachInternetGatewayResponse>"""

CREATE_INTERNET_GATEWAY_RESPONSE = u"""<CreateInternetGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2013-10-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <internetGateway>
    <internetGatewayId>{{ internet_gateway.id }}</internetGatewayId>
    <attachmentSet/>
    <tagSet>
      {% for tag in internet_gateway.get_tags() %}
        <item>
          <resourceId>{{ tag.resource_id }}</resourceId>
          <resourceType>{{ tag.resource_type }}</resourceType>
          <key>{{ tag.key }}</key>
          <value>{{ tag.value }}</value>
        </item>
      {% endfor %}
    </tagSet>
  </internetGateway>
</CreateInternetGatewayResponse>"""

DELETE_INTERNET_GATEWAY_RESPONSE = u"""<DeleteInternetGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2013-10-15/">
    <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
    <return>true</return>
</DeleteInternetGatewayResponse>"""

DESCRIBE_INTERNET_GATEWAYS_RESPONSE = u"""<DescribeInternetGatewaysResponse xmlns="http://ec2.amazonaws.com/doc/2013-10-
15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <internetGatewaySet>
    {% for igw in internet_gateways %}
    <item>
      <internetGatewayId>{{ igw.id }}</internetGatewayId>
      {% if igw.vpc  %}
        <attachmentSet>
          <item>
            <vpcId>{{ igw.vpc.id }}</vpcId>
            <state>available</state>
          </item>
        </attachmentSet>
      {% else %}
        <attachmentSet/>
      {% endif %}
      <tagSet>
        {% for tag in igw.get_tags() %}
          <item>
            <resourceId>{{ tag.resource_id }}</resourceId>
            <resourceType>{{ tag.resource_type }}</resourceType>
            <key>{{ tag.key }}</key>
            <value>{{ tag.value }}</value>
          </item>
        {% endfor %}
      </tagSet>
    </item>
    {% endfor %}
  </internetGatewaySet>
</DescribeInternetGatewaysResponse>"""

DETACH_INTERNET_GATEWAY_RESPONSE = u"""<DetachInternetGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2013-10-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <return>true</return>
</DetachInternetGatewayResponse>"""
