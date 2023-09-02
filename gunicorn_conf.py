#---------
#もしこのgunicorn_conf.pyを移動させたなら、appsディレクトリがあるところまでcdを移動させるため
#chdirを設定してください
# chdir = "crud_app"
#---------
chdir = "/home/ec2-user/blog-flask/apps"
wsgi_app = "apps.app:create_app('product')"
workers = 2
# /tmp ディレクトリにソケットができる
socket_path = 'unix:/tmp/gunicorn_flask.sock'
bind = socket_path
#開発時はreload=True
reload = True

