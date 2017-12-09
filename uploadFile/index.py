#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template
from flask_uploads import *
from flask_wtf import Form
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
app = Flask(__name__)
# 新建一个set用于设置文件类型、过滤等
set_doc = UploadSet('DOC')
# 用于wtf.quick_form()模版渲染
bootstrap = Bootstrap(app)
# DOC的存储位置
# UPLOADED_xxxxx_DEST, xxxxx部分就是定义的set的名称-DOC,下同
app.config['UPLOADED_DOC_DEST'] = './Uploads'
# DOC允许存储的类型
app.config['UPLOADED_DOC_ALLOW'] = DOCUMENTS
# 把刚刚app设置的config注册到set_doc
configure_uploads(app, set_doc)
app.config['SECRET_KEY'] = 'PYsaber'
class UploadForm(Form):
    '''
        一个简单的上传表单
    '''
    # 文件field设置为非空，过滤规则设置为‘set_doc’
    upload = FileField(u'上传文件', validators=[
                       FileRequired(), FileAllowed(set_doc, 'you can upload doc only!')])
    submit = SubmitField('ok')
@app.route('/', methods=('GET', 'POST'))
def index():
    form = UploadForm()
    url = None
    if form.validate_on_submit():
        filename = form.upload.data.filename
        url = set_doc.save(form.upload.data, name=filename)
    return render_template('index.html',form=form, url=url)
if __name__ == '__main__':
    app.run(debug=True)
