from serializers import json
import json as json2
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def insert_hq():
    insert = request.vars.insert
    data = {'title' : request.vars.hq_title,
            'description' : request.vars.hq_description,
            'year' : request.vars.hq_year,
            'characters' : json2.loads(request.vars.hq_character)}
    if insert == 'true':
        if len(db.executesql("SELECT id FROM hq WHERE hq_title='{0}' AND deleted='F'".format(data['title']),as_dict=True)) == 0:
            query = """INSERT INTO hq (created, hq_title, hq_description, hq_year, deleted)
                        VALUES ('{0}', '{1}', '{2}', '{3}', 'F') RETURNING id""".format(request.now, data['title'], data['description'], data['year'])
        else:
            return XML(json('erro'))
    else:
        item_edit = request.vars.item_edit
        if len(db.executesql("SELECT id FROM hq WHERE hq_title='{0}' AND id != {1} AND deleted='F'".format(data['title'],item_edit),as_dict=True)) == 0:
            query = """UPDATE hq SET hq_title='{0}', hq_description='{1}', hq_year='{2}' WHERE id={3} RETURNING id""".format(data['title'],
                                                                                                                             data['description'],
                                                                                                                             data['year'],
                                                                                                                             item_edit)
        else:
            return XML(json('erro'))
    try:
        id_hq = db.executesql(query,as_dict=True)
        id_hq = id_hq[0]['id']
        if insert == 'true':
            for c in data['characters']:
                db.executesql("""INSERT INTO hq_character (created, marvel_character, hq, deleted)
                                    VALUES ('{0}', {1}, {2}, 'F')""".format(request.now, c, id_hq))
        else:
            aux = ''
            for c in data['characters']:
                aux += c + ','
                if len(db.executesql("""SELECT id FROM hq_character 
                                        WHERE hq={0} AND marvel_character={1} AND deleted='F'""".format(id_hq, c),as_dict=True)) == 0:
                    db.executesql("""INSERT INTO hq_character (created, marvel_character, hq, deleted)
                                    VALUES ('{0}', {1}, {2}, 'F')""".format(request.now, c, id_hq))
            aux = aux[0:-1]
            db.executesql("UPDATE hq_character SET deleted='T' WHERE hq={0} AND marvel_character NOT IN ({1})".format(id_hq, aux))
                
                    
        ret = {'hqs' : db.executesql("SELECT id, hq_title, hq_description, hq_year FROM hq WHERE deleted='F'",as_dict=True),
               'hqs_characters' : db.executesql("SELECT id, marvel_character, hq FROM hq_character WHERE deleted='F'",as_dict=True)}
        db.commit()
    except Exception as wE:
        db.rollback()
        ret = 'erro'
            
    return XML(json(ret))

def delete_hq():
    id_del = request.vars.delete
    try:
        db.executesql("UPDATE hq SET deleted='T' WHERE id={0}".format(id_del))
        ret = {'hqs' : db.executesql("SELECT id, hq_title, hq_description, hq_year FROM hq WHERE deleted='F'",as_dict=True),
               'hqs_characters' : db.executesql("SELECT id, marvel_character, hq FROM hq_character WHERE deleted='F'",as_dict=True)}
        db.commit()
    except Exception as wE:
        db.rollback()
        ret = 'erro'
    
    return XML(json(ret))

def insert_news():
    news = {'title' : request.vars['data[news_title]'],
            'link'  : request.vars['data[news_url]'],
            'text'  : request.vars['data[news_text]']}
    insert = request.vars.insert
    try:
        if insert == 'true':
            query = """INSERT INTO news (created, news_title, news_url, news_text, deleted) 
                            VALUES (now(), '{0}', '{1}', '{2}', 'F')""".format(news['title'], news['link'], news['text'])
        else:
            query = """UPDATE news SET news_title='{0}', news_url='{1}', news_text='{2}'
                            WHERE id={3}""".format(news['title'], news['link'], news['text'], insert)
        db.executesql(query)
        db.commit()
        return ''
    except Exception as wE:
        db.rollback()
        ret = 'erro'
        return XML(json(ret))

def delete_news():
    notRemove = request.vars['data[]']
    nrstr = ''
    if notRemove == None:
        nrstr = -1
    elif type(notRemove) == str:
        nrstr = notRemove
    else:
        for i in notRemove:
            nrstr += i+','
        nrstr = nrstr[:-1]
    try:
        db.executesql("UPDATE news SET deleted='T' WHERE id NOT IN ({0})".format(nrstr))
        db.commit()
        return ''
    except Exception as wE:
        db.rollback()
        ret = 'erro'

def getNews():
    news = db.executesql("""SELECT id, news_title, created, news_text, news_url, deleted, news_image2, news_image3, news_image1
                                            FROM news WHERE deleted='F'""",as_dict=True)
    return XML(json(news))
















