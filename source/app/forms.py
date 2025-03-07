# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	company_name        = StringField  (u'Company_Name'      )
	name        		= StringField  (u'Name'      )
	username    		= StringField  (u'Username'  , validators=[DataRequired()])
	password    		= PasswordField(u'Password'  , validators=[DataRequired()])
	email       		= StringField  (u'Email'     , validators=[DataRequired(), Email()])
	phone       		= StringField  (u'Phone'     , validators=[DataRequired()])
	role        		= StringField  (u'Role'     , validators=[DataRequired()])
