import os.path
from BeautifulSoup import BeautifulSoup
from sqlalchemy.orm import subqueryload

import datamining as dm
from inphosite.model import *
from inphosite.model.meta import Session

def extract_article_body(filename):
    f=open(filename)
    doc=f.read()
    soup=BeautifulSoup(doc)

    # rip out bibliography
    biblio_root = soup.findAll('h2', text='Bibliography')
    if biblio_root:
        biblio_root = biblio_root[-1].findParent('h2')
        biblio = [biblio_root]
        biblio.extend(biblio_root.findNextSiblings())
        biblio = [elm.extract() for elm in biblio]

    # grab modified body 
    body=soup.find("div", id="aueditable")

    return body.text

def select_terms(entity_type=Idea):
    # process entities
    ideas = Session.query(entity_type)
    ideas = ideas.options(subqueryload('_spatterns'))
    # do not process Nodes or Journals
    ideas = ideas.filter(and_(Entity.typeID!=2, Entity.typeID!=4))
    return ideas.all()
     

def process_article(article, terms=None, entity_type=Idea, output_filename=None):
    if terms is None:
        terms = select_terms(entity_type)
    
    #article = Session.query(Entity).filter(entity_type.sep_dir==title).first()
    corpus_root = config['app_conf']['corpus']

    lines = []

    filename = article.get_filename(corpus_root)
    if filename and os.path.isfile(filename):
        print "processing:", article.sep_dir
        try: 
            doc = extract_article_body(filename)
            lines = dm.prepare_apriori_input(doc, terms, article)
        except:
            print "ERROR PROCESSING:", article.sep_dir
    else:
        print "BAD SEP_DIR:", article.sep_dir

    if output_filename:
        with open(output_filename, 'w') as f:
            f.writelines(lines)
    else:
        return lines

from multiprocessing import Pool

def process_articles(entity_type=Idea, output_filename='output-test.txt'):
    terms = select_terms(entity_type)
    
    articles = Session.query(entity_type).filter(entity_type.sep_dir!='').all()
    corpus_root = config['app_conf']['corpus']
   
    doc_lines = []

    for article in articles:
        lines = process_article(article, terms=terms, output_filename=None)
        doc_lines.append(lines)

    with open(output_filename, 'w') as f:
        for lines in lines:
            f.writelines(lines)

import subprocess

def complete_mining(entity_type=Idea, filename='graph.txt', root='./'):
    occur_filename = root + "graph-" + filename
    edge_filename = root + "edge-" + filename
    sql_filename = root + "sql-" + filename

    print "processing articles..."
    process_articles(entity_type, occur_filename)

    print "running apriori miner..."
    dm.apriori(occur_filename, edge_filename)
    
    print "processing edges..."
    edges = dm.process_edges(occur_filename, edge_filename)
    ents = dm.calculate_node_entropy(edges)
    edges = dm.calculate_edge_weight(edges, ents)
    
    print "creating sql files..."

    with open(sql_filename, 'w') as f:
        for edge, props in edges.iteritems():
            ante,cons = edge
            row = "%s::%s" % edge
            row += "::%(confidence)s::%(jweight)s::%(weight)s\n" % props
            f.write(row)

    print "updating term entropy..."

    for term_id, entropy in ents.iteritems():
        term = Session.query(Idea).get(term_id)
        if term:
            term.entropy = entropy

    Session.flush()
    Session.commit()

