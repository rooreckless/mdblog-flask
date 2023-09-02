#---------
#もしこのgunicorn_conf.pyを移動させたなら、appsディレクトリがあるところまでcdを移動させるため
#chdirを設定してください
# chdir = "crud_app"
#---------
chdir = "/usr/src/app/apps"
wsgi_app = "apps.app:create_app('local')"
workers = 2
# /tmp ディレクトリにソケットができる
socket_path = 'unix:/tmp/gunicorn_flask.sock'
bind = socket_path
# tcpソケット
# bind = '0.0.0.0:5000'
#開発時はreload=True
reload = True

