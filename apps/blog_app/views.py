
import json
import base64
# import markdown2
from markdown import markdown
#flaskからはMarkupを追加インポートします。
from flask import Flask,Blueprint,render_template,redirect,jsonify,request,Markup,current_app,render_template_string,url_for
import os
import boto3

#ブループリントを作成
# url_prefixを追加したBlueprintオブジェクトを作成
blog_app = Blueprint("blog_app",__name__,url_prefix="/blog_app",template_folder='templates',static_folder='static')
# blog_app = Blueprint("blog_app",__name__,url_prefix="/blog_app")


#トップページ用ルート
@blog_app.route("/",methods=["GET"],endpoint="index_route")
def index_route():
  # return render_template("blog_app/index.html")
  #現状はリダイレクトとします。
  return redirect(url_for("blog_app.show_md_route/blogstop",blog_id="blogstop"))

#markdown最終テスト用ルート
@blog_app.route("/<blog_id>",methods=["GET"],endpoint="show_md_route")
def show_md_route(blog_id):
  
  print("blog_id=",blog_id)
  
  # S3クライアントの初期化
  s3_client = boto3.client('s3',
      aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
      aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
      region_name=current_app.config['S3_REGION']
      )
  try:
    # S3からmdファイルをダウンロードし、ファイルの内容をmd_contentに格納
    response = s3_client.get_object(Bucket=current_app.config['S3_BUCKET_NAME'], Key="mdblog-content/testmd/"+blog_id+".md")
    md_content = response['Body'].read().decode('utf-8')
    
    #md_content内のimgタグの部分を公開しているs3バケットを指すように置き換える
    md_content = md_content.replace('<img src="./',
                                    '<img src="https://imagecheckhandsonnanonets.s3.ap-northeast-1.amazonaws.com/mdblog-content/testmd/')
    
    codehilite_configs = {
        #python-markdownのcodehilite用の設定
        'codehilite':{
            #mdファイル内のコードブロック```領域に当てるスタイルをpygments_styleで指定
            'pygments_style': 'dracula',
            #noclassesはTrueにしないと、pygments_styleがコードブロックに当たらない
            'noclasses': True,
            #linenums=行番号をつける
            'linenums': True,
            # guess_lang=コードブロックで使われている言語に合わせてスタイルを変える
            'guess_lang': True
            # noclasses==True && linenums==Trueなら別途cssでpreタグにline-height: 125%;が必要。
            # ないと行番号とコードがずれる
        }
    }
    #拡張機能を使用してhtmlへ変換しつつ{{md_convert}}に使われる値へ変換
    #tab_lentgh=4は空白4つで、ネストリストや、コードブロックのインデントとする
    #他の拡張機能はmdファイルのテーブル記法変換、番号付きリストと箇条書きリストの混在可設定、codehiliteを使うためのfencedcode、[TOC]を記載しておけば目次を作成してくれるtoc
    mup=Markup(markdown(md_content,
                        extensions=['attr_list','tables','sane_lists','fenced_code','codehilite','toc'],
                        extension_configs=codehilite_configs,
                        tab_length=2))
    return render_template("blog_app/blank.html",md_convert=mup)
  except Exception as e:
    #mdファイルのダウンロードに失敗した場合はエラー
    return str(e)

#-------------------------------
#ローカルでのトップページ用(blog_app/rom/)
@blog_app.route("/rom/",methods=["GET"],endpoint="index_rom_route")
def index_rom_route():
  # return render_template("blog_app/index.html")
  return redirect(url_for("blog_app.show_md_rom_route",blog_id="blogstop"))

#ローカルのmarkdown用ルート
@blog_app.route("/rom/<blog_id>",methods=["GET"],endpoint="show_md_rom_route")
def show_md_rom_route(blog_id):
  print("blog_id=",blog_id)
  
  with open('./blog_app/md/'+blog_id+'.md', mode='r') as mdfile:
    response = mdfile.read()
  md_content = response
  print("--/markdown--mdcontent=",md_content)
  # mdblog-content/testmd/main.md"
  codehilite_configs = {
        #python-markdownのcodehilite用の設定
        'codehilite':{
            #mdファイル内のコードブロック```領域に当てるスタイルをpygments_styleで指定
            'pygments_style': 'dracula',
            #noclassesはTrueにしないと、pygments_styleがコードブロックに当たらない
            'noclasses': True,
            #linenums=行番号をつける
            'linenums': True,
            # guess_lang=コードブロックで使われている言語に合わせてスタイルを変える
            'guess_lang': True
            # noclasses==True && linenums==Trueなら別途cssでpreタグにline-height: 125%;が必要。
            # ないと行番号とコードがずれる
        }
  }
  #拡張機能を使用してhtmlへ変換しつつ{{md_convert}}に使われる値へ変換
  #tab_lentgh=4は空白4つで、ネストリストや、コードブロックのインデントとする
  #他の拡張機能はmdファイルのテーブル記法変換、番号付きリストと箇条書きリストの混在可設定、codehiliteを使うためのfencedcode、[TOC]を記載しておけば目次を作成してくれるtoc
  mup=Markup(markdown(md_content,
                      extensions=['attr_list','tables','sane_lists','fenced_code','codehilite','toc'],
                      extension_configs=codehilite_configs,
                      tab_length=2))
  return render_template("blog_app/blank.html",md_convert=mup)
