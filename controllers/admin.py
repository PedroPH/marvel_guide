# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index_admin():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    x = 0
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def insert_hq():
    characters = db.executesql("SELECT id, char_name, created, char_image, char_type FROM marvel_character WHERE deleted='F'",as_dict=True)
    hqs = db.executesql("SELECT id, hq_title, hq_description, hq_year, hq_image FROM hq WHERE deleted='F'",as_dict=True)
    hqs_characters = db.executesql("SELECT id, marvel_character, hq FROM hq_character WHERE deleted='F'",as_dict=True)
    response.flash = T("Hello World")
    return dict(characters=characters,hqs=hqs,hqs_characters=hqs_characters)

def insert_news():
    return dict()