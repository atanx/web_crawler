#!/usr/bin/env python
# coding=utf-8

from flask.ext.wtf import Form
from wtforms import SelectField, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length


class SiteForm(Form):
	group_names = SelectField(u'Site分组', coerce=int, validators=[DataRequired()])
	site_list = TextAreaField(u'当前sites', validators=[DataRequired])
	new_site_list = TextAreaField(u'新sites', validators=[DataRequired])


class AddSiteForm(Form):
	group_name = StringField(label=u"site分组", validators=[DataRequired()])
