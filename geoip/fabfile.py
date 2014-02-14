from fabric.api import *


def setup_prod():
    env.hosts = ['cb101.public.cbitlabs.com']
    env.server_path = '/home/ubuntu/tmp/'
    env.python_path = '/home/ubuntu/.virtualenvs/geoip/bin'
    env.user = 'ubuntu'
    env.graceful = True


def deploy_prod():
    deploy_code()

    install_reqs()


def deploy_code():

    run("rm -rf %s/*" % env.server_path)
    local('zip -r code.zip * -x "*.pyc" "*.git"')
    put("code.zip", "%s/" % env.server_path)
    run("cd %s; unzip -o code.zip" % env.server_path)
    run("cd %s; rm -f code.zip" % env.server_path)
    local("rm -f code.zip")


def install_reqs():
    run('python %s/activate_this.py' % env.python_path)
    run('%s/pip install -r %s/requirements.txt' %
       (env.python_path, env.server_path))


def deploy_static():
    with cd(env.server_path):
        run('%s/python manage.py collectstatic -v0 --noinput' %
           (env.python_path))


def compress_static():
    with cd(env.server_path):
        run('%s/python manage.py compress --force' % (env.python_path))


def restart_apache():
    if env.graceful:
        sudo("/usr/sbin/apache2ctl -k graceful")
    else:
        sudo("service apache2 restart")
