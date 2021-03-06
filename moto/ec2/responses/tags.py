from __future__ import unicode_literals
from jinja2 import Template

from moto.core.responses import BaseResponse
from moto.ec2.models import validate_resource_ids
from moto.ec2.utils import sequence_from_querystring, tags_from_query_string, filters_from_querystring
from xml.sax.saxutils import escape


class TagResponse(BaseResponse):

    def create_tags(self):
        resource_ids = sequence_from_querystring('ResourceId', self.querystring)
        validate_resource_ids(resource_ids)
        self.ec2_backend.do_resources_exist(resource_ids)
        tags = tags_from_query_string(self.querystring)
        self.ec2_backend.create_tags(resource_ids, tags)
        return CREATE_RESPONSE

    def delete_tags(self):
        resource_ids = sequence_from_querystring('ResourceId', self.querystring)
        validate_resource_ids(resource_ids)
        tags = tags_from_query_string(self.querystring)
        self.ec2_backend.delete_tags(resource_ids, tags)
        return DELETE_RESPONSE

    def describe_tags(self):
        filters = filters_from_querystring(querystring_dict=self.querystring)
        tags = self.ec2_backend.describe_tags(filters=filters)
        for tag in tags:
            tag['value'] = escape(tag['value'])
        template = Template(DESCRIBE_RESPONSE)
        return template.render(tags=tags)


CREATE_RESPONSE = """<CreateTagsResponse xmlns="http://ec2.amazonaws.com/doc/2012-12-01/">
  <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
  <return>true</return>
</CreateTagsResponse>"""

DELETE_RESPONSE = """<DeleteTagsResponse xmlns="http://ec2.amazonaws.com/doc/2012-12-01/">
   <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
   <return>true</return>
</DeleteTagsResponse>"""

DESCRIBE_RESPONSE = """<DescribeTagsResponse xmlns="http://ec2.amazonaws.com/doc/2012-12-01/">
   <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
   <tagSet>
      {% for tag in tags %}
          <item>
             <resourceId>{{ tag.resource_id }}</resourceId>
             <resourceType>{{ tag.resource_type }}</resourceType>
             <key>{{ tag.key }}</key>
             <value>{{ tag.value }}</value>
          </item>
      {% endfor %}
    </tagSet>
</DescribeTagsResponse>"""
