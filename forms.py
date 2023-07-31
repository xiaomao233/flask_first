from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
'''
使用WTF需要自定义表单类
相当于原来的<form><label>xx</label><input type=""></form>
'''
#定义文件提交表单
class UploadFileForm(FlaskForm):
    landfile = FileField(u'请上传您的地块文件')

    submit = SubmitField(u'提交')