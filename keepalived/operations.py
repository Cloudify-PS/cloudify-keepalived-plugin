from fabric.api import settings, run

from cloudify import ctx


TARGET_PATH = "/etc/keepalived/keepalived.conf"
config = '''
vrrp_instance %(group)s {
 state %(state)s
 interface eth0
 virtual_router_id %(router_id)s
 priority %(priority)s
 authentication {
  auth_type PASS
  auth_pass password
 }
 virtual_ipaddress {
  %(internal_ip)s
 }
 advert_int %(advert_interval)s
  %(preempt)s
}
'''


def create_config_file():
    properties = dict.copy(ctx.node.properties)
    if properties['state'] == 'MASTER':
        properties['preempt'] = 'nopreempt'
    else:
        properties['preempt'] = ''
    updated_config = config % properties
    run('sudo tee {0} <<EOF \n{1}\nEOF'.format(TARGET_PATH, updated_config))


def create(fabric_env, **kwargs):
    with settings(**fabric_env):
        run('sudo yum install keepalived -y')
        create_config_file()
        run('sudo service keepalived restart')


def stop(fabric_env, **kwargs):
    with settings(**fabric_env):
        run('sudo service keepalived stop')
