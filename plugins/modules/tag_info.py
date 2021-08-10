#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing_extensions import Required
from requests.api import request
from plugins.module_utils.quay import QuayBase


DOCUMENTATION = '''
module: tags_info
short_description: Query Quay Tags info.
extends_documentation_fragment: lego963.quay.quay
version_added: "0.0.1"
author: "Rodion Gyrbu (@lego963)"
description:
  - This interface is used to query Quay Tags info based on search criteria.
options:
  repository:
    description: The full path of the repository. e.g. namespace/name
    type: str
    required: True
  only_active_tags:
    description: Filter to only active tags.
    type: bool
  page:
    description: Page index for the results.
    type: int
  limit:
    description: Limit to the number of results to return per page.
    type: int
  specific_tag:
    description: Filters the tags to the specific tag.
    type: str
'''

RETURN = '''
quay_tags:
  description:
  type: complex
  returned: success
  contains:
    name:
      description:
        - Specifies the tag name.
      type: str
      sample: "latest"
    reversion:
      description:
        - Specifies the revision status.
      type: bool
      sample: false
    start_ts:
      description:
        - Specifies the start timestamp.
      type: int
      sample: 1617711789
    image_id:
      description:
        - Specifies the image ID.
      type: str
      sample: "0b9fa0b7f59414a64fbee47c7542217909614ebd1046520657e54c34f4af3b47"
    last_modified:
      description:
        - Specifies the instance ID.
      type: str
      sample: "Tue, 06 Apr 2021 13:46:29 -0000"
    manifest_digest:
      description:
        - Specifies the manifest digest.
      type: str
      sample: "sha256:b5557b4f77e7382b3203b940aaa050286e8f201d13520c169fdd2cab5bc3b88a"
    docker_image_id:
      description:
        - Specifies the docker image ID.
      type: str
      sample: "0b9fa0b7f59414a64fbee45c7542517909614ebd1046520657e54c34f4af3b47"
    is_manifest_list:
      description:
        - Specifies the manifest list status.
      type: bool
      sample: false
    size:
      description:
        - Specifies the image size.
      type: int
      sample: 293412157
'''

EXAMPLES = '''
# Get all Quay Tags
- lego963.quay.tags_info:
    repository: "opentelekomcloud/apimon"
  register: quay_tags

# Get only active Quay Tags
- lego963.quay.tags_info:
    repository: "opentelekomcloud/apimon"
    only_active_tags: true
  register: filtered_quay_tags
'''


class TagsModule(QuayBase):
    argument_spec = dict(
        repository=dict(type='str', required=True),
        page=dict(type='int', required=False),
        limit=dict(type='int', required=False),
        specific_tag=dict(type='str', required=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False
        repository = self.params['repository']
        query = {
            'only_active_tags': self.params['only_active_tags'],
            'page': self.params['page'],
            'limit': self.params['limit'],
            'specificTag': self.params['specific_tag'],
        }

        repo_tags = self.get_tags(repository, query=query)
        if repo_tags is None:
            self.fail_json(
                msg=f'Cannot fetch repository tags for {repository}',
                errors=self.errors)

        if len(self.errors) == 0:
            self.exit_json(
                changed=changed,
                errors=self.errors,
                quay_tags=repo_tags['tags']
            )
        else:
            self.fail_json(
                changed=changed,
                msg='Failures occured',
                errors=self.errors,
            )


def main():
    module = TagsModule()
    module()


if __name__ == "__main__":
    main()
