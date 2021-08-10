# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import abc

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib


def base_argument_spec(**kwargs):
    spec = dict(
        quay_url=dict(type='str', default='https://quay.io/api/v1')
    )
    spec.update(kwargs)
    return spec


class QuayBase:
    argument_spec = {}
    module_kwargs = {}
    _bp_templates = {}

    def __init__(self):
        self.ansible = AnsibleModule(
            base_argument_spec(**self.argument_spec),
            **self.module_kwargs)
        self.params = self.ansible.params
        self.module_name = self.ansible._name
        self.sdk_version = None
        self.results = {'changed': False}
        self.exit = self.exit_json = self.ansible.exit_json
        self.fail = self.fail_json = self.ansible.fail_json
        self.quay_url = self.params['quay_url']
        self.errors = []

    @abc.abstractmethod
    def run(self):
        pass

    def __call__(self):
        """Execute `run` function when calling the class.
        """

        if not HAS_REQUESTS:
            self.fail_json(msg=missing_required_lib('requests'))

        try:
            results = self.run()
            if results and isinstance(results, dict):
                self.ansible.exit_json(**results)
        except Exception as ex:
            msg = str(ex)
            self.ansible.fail_json(msg=msg, errors=self.errors)

    def save_error(self, msg):
        self.errors.append(msg)

    def request(self, method='GET', url=None, headers=None, timeout=15, query=None, **kwargs):
        if not headers:
            headers = dict()

        if not url.startswith('http'):
            url = f"{self.quay_url}/{url}"

        return requests.request(
            method, url, headers=headers, timeout=timeout, params=query, **kwargs)

    def get_tags(self, repository, query):
        """Get Quay Tags"""

        rsp = self.request(
            method='GET',
            url=f'repository/{repository}/tag/',
            query=query
        )
        if rsp.status_code not in [200]:
            self.save_error(f"Cannot fetch repository {repository} tags")

        return rsp.json()
