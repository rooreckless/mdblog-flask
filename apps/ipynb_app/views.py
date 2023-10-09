
import json
import base64
# import markdown2
from markdown import markdown
#flaskからはMarkupを追加インポートします。
from flask import Flask,Blueprint,render_template,redirect,jsonify,request,Markup,current_app,render_template_string,url_for
import os
import boto3
import pdb

#ブループリントを作成
# url_prefixを追加したBlueprintオブジェクトを作成
ipynb_app = Blueprint("ipynb_app",__name__,url_prefix="/ipynb_app",template_folder='templates',static_folder='static')


#トップページ用ルート
@ipynb_app.route("/",methods=["GET"],endpoint="index_route")
def index_route():
  # return render_template("ipynb_app/index.html")
  #現状はリダイレクトとします。
  return redirect(url_for("ipynb_app.show_ipynb_route",ipynb_id="ipynbstop"))

#ipynb用ルート
@ipynb_app.route("/<pynb_id>",methods=["GET"],endpoint="show_md_route")
def show_ipynb_route(ipynb_id):
  
  # S3クライアントの初期化
  s3_client = boto3.client('s3',
      aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
      aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
      region_name=current_app.config['S3_REGION']
      )
  try:
    # S3からmdファイルをダウンロードし、ファイルの内容をipynb_contentに格納
    response = s3_client.get_object(Bucket=current_app.config['S3_BUCKET_NAME'], Key="mdblog-content/testipynb/"+ipynb_id+".html")
    ipynb_content = response['Body'].read().decode('utf-8')

    #ipynb_content内のimgタグの部分を公開しているs3バケットを指すように置き換える
    ipynb_content = ipynb_content.replace(' alt="No description has been provided for this image"','')
    ipynb_content = ipynb_content.replace('<img src="./img','<img src="https://imagecheckhandsonnanonets.s3.ap-northeast-1.amazonaws.com/mdblog-content/testipynb/img')
    
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
    mup=Markup(markdown(ipynb_content,
                        extensions=['attr_list','tables','sane_lists','fenced_code','codehilite','toc'],
                        extension_configs=codehilite_configs,
                        tab_length=2))
    return render_template("ipynb_app/blank.html",html_content=mup)
  except Exception as e:
    #mdファイルのダウンロードに失敗した場合はエラー
    return str(e)

#-------------------------------
#ローカルでのトップページ用(ipynb_app/rom/)
@ipynb_app.route("/rom/",methods=["GET"],endpoint="index_rom_route")
def index_rom_route():
  # return render_template("ipynb_app/index.html")
  return redirect(url_for("ipynb_app.show_ipynb_rom_route",ipynb_id="ipynbstop"))

#ローカルのmarkdown用ルート
@ipynb_app.route("/rom/<ipynb_id>",methods=["GET"],endpoint="show_ipynb_rom_route")
def show_ipynb_rom_route(ipynb_id):
  print("ipynb_id=",ipynb_id)
  
  with open('./ipynb_app/converted_html/'+ipynb_id+'.html', mode='r') as htmlfile:
    response = htmlfile.read()
  ipynb_content = response
  #ipynbが画像を読み込んでいると、imgタグにalt属性がついているので削除します。その後s3のフォルダを指します。
  #(あくまでデバッグ用のため実際に画像表示はさせませんが。)
  ipynb_content = ipynb_content.replace(' alt="No description has been provided for this image"','')
  ipynb_content = ipynb_content.replace('<img src="./img','<img src="https://imagecheckhandsonnanonets.s3.ap-northeast-1.amazonaws.com/mdblog-content/testipynb/img')
  
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
  mup=Markup(markdown(ipynb_content,
                      extensions=['attr_list','tables','sane_lists','fenced_code','codehilite','toc'],
                      extension_configs=codehilite_configs,
                      tab_length=2))
  return render_template("ipynb_app/blank.html",html_content=mup)
