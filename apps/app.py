#app.py
from flask import Flask

#ブループリントback_appのviews.pyをインポート
from apps.blog_app import views


def create_app(config_key):
  app=Flask(__name__)
  app.register_blueprint(views.blog_app,url_prefix="/blog_app")

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