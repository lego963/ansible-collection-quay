# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Standard documentation fragment
    DOCUMENTATION = r'''
options:
  repository:
    description:
      - Root path to the configuration location.
    type: str
    required: True
  only_active_tags:
    description:
      - Filter to only active tags.
    type: bool
    required: False
  page:
    description:
      - Page index for the results.
    type: int
    required: False
  limit:
    description:
      - Limit to the number of results to return per page.
    type: int
    required: False
  specific_tag:
    description:
      - Filters the tags to the specific tag.
    type: str
    required: False
  quay_url:
    description: URL of the Quay API
    type: str
    default: https://quay.io/api/v1
requirements:
  - python >= 3.6
  - requests
'''
