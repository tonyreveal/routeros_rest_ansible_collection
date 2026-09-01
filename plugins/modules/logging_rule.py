#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: logging_rule
short_description: Manage or gather RouterOS logging rule information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates, updates, or removes a RouterOS system logging rule.
  - Uses the topics and action together to identify the managed rule.
  - Verifies that the requested logging action already exists before managing the rule.
  - The rule is enabled by default.
  - The module does not create Ansible facts.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host:
    description: RouterOS REST base URL.
    type: str
    required: true
  username:
    description: RouterOS REST username.
    type: str
    required: true
  password:
    description: RouterOS REST password.
    type: str
    required: true
    no_log: true
  topics:
    description: List of RouterOS log topics, including optional ! exclusions.
    type: list
    elements: str
    required: true
  action:
    description: Existing RouterOS logging action name.
    type: str
    required: true
  enabled:
    description: Whether the logging rule should be enabled.
    type: bool
    default: true
  comment:
    description: Optional rule comment.
    type: str
    default: ''
  prefix:
    description: Optional text prefix added to matching log messages.
    type: str
    default: ''
  regex:
    description: Optional regular expression used to filter matching messages.
    type: str
    default: ''
  state:
    description: Whether the logging rule should exist.
    type: str
    choices: [absent, present]
    default: present
  validate_certs:
    description: Validate the RouterOS www-ssl certificate.
    type: bool
    default: true
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
requirements:
  - Python 3
  - RouterOS 7.x with the www-ssl or www REST service enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Send critical and error logs to email-alerts
  mikrotik.routeros.logging_rule:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    topics:
      - critical
      - error
    action: email-alerts
    enabled: true
    comment: Critical and error email notifications
    prefix: ALERT

- name: Remove a logging rule
  mikrotik.routeros.logging_rule:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    topics:
      - critical
      - error
    action: email-alerts
    state: absent
...
"""


RETURN = r"""
rule:
  description: RouterOS logging rule returned after reconciliation.
  returned: success
  type: raw
changed_fields:
  description: Rule fields changed during this invocation.
  returned: success
  type: list
"""


def _first_record(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value if isinstance(value, dict) else None


def _normalise_topics(value):
    if isinstance(value, list):
        topics = value
    else:
        topics = str(value).split(",")
    return sorted({str(topic).strip() for topic in topics if str(topic).strip()})


def _bool_matches(current, desired):
    return (str(current).lower() in {"yes", "true"}) == desired


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "topics": {"type": "list", "elements": "str", "required": True, "min": 1},
            "action": {"type": "str", "required": True},
            "enabled": {"type": "bool", "default": True},
            "comment": {"type": "str", "default": ""},
            "prefix": {"type": "str", "default": ""},
            "regex": {"type": "str", "default": ""},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    topics = _normalise_topics(params["topics"])
    if not topics:
        module.fail_json(msg="topics must contain at least one non-empty topic")
    if not params["action"].strip():
        module.fail_json(msg="action must not be empty")

    desired = {
        "topics": ",".join(topics),
        "action": params["action"],
        "disabled": not params["enabled"],
        "comment": params["comment"],
        "prefix": params["prefix"],
        "regex": params["regex"],
    }
    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    try:
        actions = client.get("system/logging/action", query={"name": params["action"]})
        if not actions or (isinstance(actions, list) and not any(isinstance(item, dict) for item in actions)):
            module.fail_json(msg=f"RouterOS logging action does not exist: {params['action']}")

        rules = client.get("system/logging")
        if not isinstance(rules, list):
            rules = [rules]
        matches = [
            rule for rule in rules
            if isinstance(rule, dict)
            and _normalise_topics(rule.get("topics", "")) == topics
            and str(rule.get("action", "")) == params["action"]
        ]
        if len(matches) > 1:
            module.fail_json(msg="Multiple RouterOS logging rules match the requested topics and action")
        existing = matches[0] if matches else None

        if params["state"] == "absent":
            if existing is None:
                module.exit_json(changed=False, rule={}, changed_fields=[])
            resource_id = existing.get(".id")
            if not resource_id:
                module.fail_json(msg="RouterOS logging rule response did not include .id")
            result = existing if module.check_mode else client.delete(f"system/logging/{resource_id}")
            module.exit_json(changed=True, rule=result, changed_fields=["rule"])

        if existing is None:
            result = desired if module.check_mode else client.put("system/logging", desired)
            module.exit_json(changed=True, rule=result, changed_fields=list(desired))

        resource_id = existing.get(".id")
        if not resource_id:
            module.fail_json(msg="RouterOS logging rule response did not include .id")
        changes = {}
        for key, value in desired.items():
            if key == "topics":
                if _normalise_topics(existing.get(key, "")) != topics:
                    changes[key] = value
            elif key == "disabled":
                if not _bool_matches(existing.get(key, "no"), value):
                    changes[key] = value
            elif str(existing.get(key, "")) != str(value):
                changes[key] = value
        if not changes:
            module.exit_json(changed=False, rule=existing, changed_fields=[])
        result = {**existing, **changes} if module.check_mode else client.patch(
            f"system/logging/{resource_id}", changes
        )
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, rule=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()
