#app.py
from flask import Flask

#ブループリントback_appのviews.pyをインポート
from apps.blog_app import views as blog_app_views
#ブループリントipynb_appのviews.pyをインポート asで名称変更必須
from apps.ipynb_app import views as ipynb_app_views

def create_app(config_key):
  app=Flask(__name__)
  app.register_blueprint(blog_app_views.blog_app,url_prefix="/blog_app")
  app.register_blueprint(ipynb_app_views.ipynb_app,url_prefix="/ipynb_app")

  # app.config.from_object(config[config_key])
  if config_key=="product":
    print("create_app----config_key=",config_key)
    app.config.from_pyfile("../.env.py")
  elif config_key=="local":
    print("create_app----config_key=",config_key)
    app.config.from_pyfile("../dev.env.py")
  else:
    print("create_app----config_key=",config_key)
    app.config.from_pyfile("../dev.env.py")
  return app
if __name__=="__main__":
    app=create_app()
    