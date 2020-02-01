import os
import json
from jsonpath_ng import jsonpath, parse


import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('instance-master')


def test_k3s_running_and_enabled(host):
    k3s = host.service("k3s")
    assert k3s.is_running
    assert k3s.is_enabled
 
def test_k3s_nodes_command_output(host):
    command = host.run("k3s kubectl get nodes -o=json")
    jsonResponse = json.loads(command.stdout)
    jsonParserNodeName = parse('items[*].metadata.name')
    assert len(jsonParserNodeName.find(jsonResponse)) == 2
    assert command.rc == 0