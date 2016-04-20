# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
from datetime import datetime
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('postgres://postgres:aq1sw2DE#FR$@localhost/marvel_guide',pool_size=5,check_reserved=['all'],
                    fake_migrate=True)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('marvel_character',
    Field('char_name',requires=IS_NOT_EMPTY(),unique=True,length=128,label='Nome'),
    Field('created','datetime',label='Criado',default=datetime.now()),
    Field('char_image',type='upload',uploadfolder='applications/transit/uploads/province/',label='Imagem'),
    Field('char_type','integer',requires=IS_NOT_EMPTY(),label='Tipo do Personagem'),
    Field('deleted','boolean',label='Deleção Lógica',default='F'))

db.define_table('hq',
    Field('hq_title',requires=IS_NOT_EMPTY(),unique=True,length=128,label='Nome'),
    Field('created','datetime',label='Criado',default=datetime.now()),
    Field('hq_image',type='upload',uploadfolder='applications/transit/uploads/province/',label='Imagem'),
    Field('hq_year',length=4,requires=IS_NOT_EMPTY(),label='Ano'),
    Field('hq_description',length=500,label='Descrição'),
    Field('deleted','boolean',label='Deleção Lógica',default='F'))

db.define_table('hq_character',
    Field('created','datetime',label='Criado',default=datetime.now()),
    Field('marvel_character',db.marvel_character,requires=IS_EMPTY_OR(IS_IN_DB(db, 'marvel_character.id', '%(char_name)s')), 
              represent=lambda id, row: db.marvel_character(id).char_name if id else '',label='Personagem'),
    Field('hq',db.hq,requires=IS_EMPTY_OR(IS_IN_DB(db, 'hq.id', '%(hq_title)s')),
              represent=lambda id, row: db.hq(id).hq_title if id else '',label='HQ'),
    Field('deleted','boolean',label='Deleção Lógica',default='F'))

db.hq_character.marvel_character.requires = IS_IN_DB(db,'marvel_character.id','%(char_name)s',zero=T('Selecione'))
db.hq_character.hq.requires = IS_IN_DB(db,'hq.id','%(hq_title)s',zero=T('Selecione'))