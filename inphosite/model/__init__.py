"""The application's model objects"""
import sqlalchemy as sa

from inphosite.model import meta
from inphosite.model.entity import *
from inphosite.model.idea import * 
from inphosite.model.thinker import *
from inphosite.model.journal import * 
from inphosite.model.taxonomy import *
from inphosite.model.graph import *
from inphosite.model.user import *
from inphosite.model.school_of_thought import *
from inphosite.model.work import *
from inphosite.model.sepentry import *

from sqlalchemy import schema, types
from sqlalchemy.sql.expression import and_, or_, not_

# import schema and orm tools 
#from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.orm import *
from sqlalchemy.types import *

def init_model(engine):
    """
    This function initializes the ontology model for the given engine.
    This must be called before using the model. 

    Tables are defined first and then relations mapped to them.

    """
    meta.Session.configure(bind=engine)
    meta.engine = engine

    #define entity tables
    global entity_table
    entity_table = Table('entity', meta.metadata,
        Column('ID', Integer, primary_key=True),
        Column('label', Unicode),
        Column('searchstring', Unicode),
        autoload=True, autoload_with=engine)
    
    global searchpatterns_table
    searchpatterns_table = Table('searchpatterns', meta.metadata,
        Column('searchpattern', Unicode, primary_key=True),
        Column('target_id', ForeignKey('entity.ID'), primary_key=True),
        autoload=True, autoload_with=engine)

    #define idea tables
    global idea_table
    idea_table = Table('idea', meta.metadata,
        Column('ID', ForeignKey('entity.ID'), primary_key=True),
        autoload=True, autoload_with=engine)

    global idea_link_to_table
    idea_link_to_table = Table('idea_link_to', meta.metadata,
        Column('source_id', ForeignKey('idea.ID')),
        Column('target_id', ForeignKey('idea.ID')),
        autoload=True, autoload_with=engine)

    global idea_instance_of_table
    idea_instance_of_table = Table('idea_instance_of', meta.metadata,
        Column('instance_id', ForeignKey('idea.ID')),
        Column('class_id', ForeignKey('idea.ID')),
        autoload=True, autoload_with=engine)

    global idea_graph_edges_table
    idea_graph_edges_table = Table('idea_graph_edges', meta.metadata,
        Column('ID', Integer, primary_key=True),
        Column('ante_id', ForeignKey('idea.ID')),
        Column('cons_id', ForeignKey('idea.ID')),
        autoload=True, autoload_with=engine)
    
    global idea_thinker_graph_edges_table
    idea_thinker_graph_edges_table = Table('idea_thinker_graph_edges', meta.metadata,
        Column('ID', Integer, primary_key=True),
        Column('ante_id', ForeignKey('entity.ID')),
        Column('cons_id', ForeignKey('entity.ID')),
        autoload=True, autoload_with=engine)
    
    global thinker_graph_edges_table
    thinker_graph_edges_table = Table('thinker_graph_edges', meta.metadata,
        Column('ante_id', ForeignKey('thinker.ID'), primary_key=True),
        Column('cons_id', ForeignKey('thinker.ID'), primary_key=True),
        autoload=True, autoload_with=engine)

    global ontotree_table
    ontotree_table = Table('ontotree', meta.metadata,
        Column('ID', ForeignKey('entity.ID'), primary_key=True),
        Column('concept_id', ForeignKey('idea.ID')),
        Column('area_id', ForeignKey('idea.ID')),
        Column('parent_concept_id', ForeignKey('idea.ID')),
        Column('parent_id', ForeignKey('ontotree.ID')), 
        autoload=True, autoload_with=engine)

    # note - when moving to new schema, will need to change this table's ORM
    global idea_evaluation_table
    idea_evaluation_table = Table('idea_evaluation', meta.metadata,
        Column('ID', Integer, primary_key=True),
        Column('cons_id', ForeignKey('idea.ID')),
        Column('ante_id', ForeignKey('idea.ID')),
        Column('uid', ForeignKey('inpho_user.ID')),
        autoload=True, useexisting=True, autoload_with=engine)
    
    global anon_evaluation_table
    anon_evaluation_table = Table('anon_eval', meta.metadata,
        Column('ip', String, primary_key=True),
        Column('cons_id', ForeignKey('idea.ID'), primary_key=True),
        Column('ante_id', ForeignKey('idea.ID'), primary_key=True),
        autoload=True, useexisting=True, autoload_with=engine)
    

    #define thinker tables
    global thinker_table
    thinker_table = Table('thinker', meta.metadata,
        Column('ID', ForeignKey('entity.ID'), primary_key=True),
        autoload=True, autoload_with=engine, useexisting=True)
    
    global nationality_table
    nationality_table = Table('nationality', meta.metadata,
        Column('ID', Integer, primary_key=True),
        autoload=True, autoload_with=engine)
    
    global thinker_has_nationality
    thinker_has_nationality_table = Table('thinker_has_nationality', meta.metadata,
        Column('thinker_id', ForeignKey('thinker.ID')),
        Column('value', ForeignKey('nationality.ID')),
        autoload=True, autoload_with=engine)

    global profession_table
    profession_table = Table('profession', meta.metadata,
        Column('id', Integer, primary_key=True),
        autoload=True, autoload_with=engine)
    
    global thinker_has_profession_table
    thinker_has_profession_table = Table('thinker_has_profession', meta.metadata,
        Column('thinker_id', ForeignKey('thinker.ID')),
        Column('value', ForeignKey('profession.id')),
        autoload=True, autoload_with=engine)

    global alias_table
    alias_table = Table('alias', meta.metadata,
        Column('thinker_id', ForeignKey('entity.ID'), primary_key=True),
        Column('value', Integer, primary_key=True),
        autoload=True, autoload_with=engine)

    global thinker_has_influenced_evaluation_table
    thinker_has_influenced_evaluation_table = Table('thinker_has_influenced_evaluation', meta.metadata,
        Column('thinker1_id', ForeignKey('thinker.ID'), primary_key=True),
        Column('thinker2_id', ForeignKey('thinker.ID'), primary_key=True),
        Column('uid', ForeignKey('inpho_user.ID'), primary_key=True),
        autoload=True, autoload_with=engine)

    global thinker_teacher_of_evaluation_table
    thinker_teacher_of_evaluation_table = Table('thinker_teacher_of_evaluation', meta.metadata,
        Column('thinker1_id', ForeignKey('thinker.ID'), primary_key=True),
        Column('thinker2_id', ForeignKey('thinker.ID'), primary_key=True),
        Column('uid', ForeignKey('inpho_user.ID'), primary_key=True),
        autoload=True, autoload_with=engine)

    # Journal tables
    global journal_table
    journal_table = Table('journal', meta.metadata,
        Column('ID', ForeignKey('entity.ID'), primary_key=True),
        autoload=True, autoload_with=engine)

    global journal_abbr_table
    journal_abbr_table = Table('journal_abbr', meta.metadata,
        Column('id', Integer, primary_key=True),
        Column('journal_id', ForeignKey('journal.ID')),
        autoload=True, autoload_with=engine)

    global journal_search_query_table
    journal_search_query_table = Table('journal_search_query', meta.metadata,
        Column('id', Integer, primary_key=True),
        Column('journal_id', ForeignKey('journal.ID')),
        Column('value', String),
        autoload=True, autoload_with=engine)

    # Group tables
    global school_of_thought_table
    school_of_thought_table = Table('school_of_thought', meta.metadata,
        Column('ID', ForeignKey('entity.ID'), primary_key=True),
        autoload=True, autoload_with=engine)
    
    # Work tables
    global work_table
    work_table = Table('work', meta.metadata,
        Column('ID', ForeignKey('entity.ID'), primary_key=True),
        autoload=True, autoload_with=engine)

    # User tables
    global user_table
    user_table = Table('inpho_user', meta.metadata,
        Column('ID', Integer, primary_key=True),
        Column('first_area_concept_id', ForeignKey('idea.ID')),
        Column('second_area_concept_id', ForeignKey('idea.ID')),
        Column("group_uid", ForeignKey("groups.uid")),
        autoload=True, autoload_with=engine)

    global sep_area_table
    sep_area_table = Table('sep_areas', meta.metadata,
        Column('id', Integer, primary_key=True),
        Column('concept_id', ForeignKey('idea.ID')),
        autoload=True, autoload_with=engine)
    
    global sepentries_table
    sepentries_table = Table('sepentries', meta.metadata,
        Column('sep_dir', String, unique=True, nullable=False, primary_key=True),
        Column('title', String, unique=True, nullable=False),
        Column('published', Boolean, nullable=False),
        Column('status', String, nullable=False),
        autoload=True, autoload_with=engine
    )
    
    global fuzzymatches_table
    fuzzymatches_table = Table('fuzzymatches', meta.metadata,
        Column('sep_dir', ForeignKey('sepentries.sep_dir'), primary_key=True),
        Column('entityID', ForeignKey('entity.ID'), primary_key=True),
        Column('strength', Numeric),
        Column('edits', Numeric),
        autoload=True, autoload_with=engine)
    
    global groups_table
    groups_table = Table(
            "groups",
            meta.metadata,
            Column("uid", Integer, primary_key=True),
            Column("name", String, unique=True,    nullable=False),
        )
    global roles_table
    roles_table = Table(
            "roles",
            meta.metadata,
            Column("uid", Integer, primary_key=True),
            Column("name", String, unique=True,    nullable=False),
        )
    
    global users_roles_table
    users_roles_table = Table(                # many:many relation table
            "users_roles",
            meta.metadata,
            Column("user_uid", ForeignKey("inpho_user.ID")),
            Column("role_uid", ForeignKey("roles.uid")),
        )

    #define idea relations
    mapper(Entity, entity_table, polymorphic_on=entity_table.c.typeID, polymorphic_identity=0, properties={
        'alias':relation(Alias), 
        #'spatterns':relation(SearchPattern),
            'spatterns':relation(SearchPattern, 
            cascade="all,delete-orphan"),
            })
    
    mapper(Idea, idea_table, inherits=Entity, polymorphic_on=entity_table.c.typeID, polymorphic_identity=1, properties={
        'links':relation(Idea, secondary=idea_link_to_table,
            primaryjoin=(idea_table.c.ID == idea_link_to_table.c.source_id),
            secondaryjoin=(idea_table.c.ID == idea_link_to_table.c.target_id),
            order_by=idea_table.c.entropy.asc(),
            backref=backref('links_to', order_by=idea_table.c.entropy.desc()),
            cascade="all, delete"
            ),
        'instances':relation(Idea, secondary=idea_instance_of_table,
            primaryjoin=(idea_table.c.ID == idea_instance_of_table.c.class_id),
            secondaryjoin=(idea_table.c.ID == idea_instance_of_table.c.instance_id),
            order_by=idea_table.c.entropy.desc(),
            backref=backref('instance_of', order_by=idea_table.c.entropy.desc()),
            cascade="all, delete"
            ),
        'nodes':relation(Node, secondary=ontotree_table, viewonly=True,
            primaryjoin=(idea_table.c.ID == ontotree_table.c.concept_id),
            secondaryjoin=(ontotree_table.c.concept_id == idea_table.c.ID),
            order_by=idea_table.c.entropy.desc(),
            #backref=backref('idea'),
            cascade="all, delete"
            ),
        'evaluations':relation(Node, secondary=idea_evaluation_table,
            primaryjoin=(idea_table.c.ID == idea_evaluation_table.c.ante_id),
            secondaryjoin=(idea_evaluation_table.c.ante_id == idea_table.c.ID),
            order_by=idea_evaluation_table.c.relatedness.desc(),
            cascade="all, delete"
            ),
        'hyponyms':dynamic_loader(Idea, secondary=idea_graph_edges_table,
            primaryjoin=and_(idea_table.c.ID == idea_graph_edges_table.c.cons_id, 
                             idea_graph_edges_table.c.weight > 0),
            secondaryjoin=(idea_graph_edges_table.c.ante_id == idea_table.c.ID),
            order_by=idea_graph_edges_table.c.weight.desc(),
            ),
        'occurrences':dynamic_loader(Idea, secondary=idea_graph_edges_table,
            primaryjoin=and_(idea_table.c.ID == idea_graph_edges_table.c.cons_id, 
                             idea_graph_edges_table.c.occurs_in > 0),
            secondaryjoin=(idea_graph_edges_table.c.ante_id == idea_table.c.ID),
            order_by=idea_graph_edges_table.c.occurs_in.desc(),
            ),
        'thinker_occurrences':dynamic_loader(Thinker, secondary=idea_thinker_graph_edges_table,
            primaryjoin=and_(entity_table.c.ID == idea_thinker_graph_edges_table.c.cons_id, 
                             idea_thinker_graph_edges_table.c.occurs_in > 0),
            secondaryjoin=(idea_thinker_graph_edges_table.c.ante_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.occurs_in.desc(),
            ),
        'related':dynamic_loader(Idea, secondary=idea_graph_edges_table,
            primaryjoin=(idea_table.c.ID == idea_graph_edges_table.c.ante_id),
            secondaryjoin=(idea_graph_edges_table.c.cons_id == idea_table.c.ID),
            order_by=idea_graph_edges_table.c.jweight.desc(),
            ),
        'evaluated':dynamic_loader(Idea, secondary=idea_evaluation_table,
            primaryjoin=and_(idea_table.c.ID == idea_evaluation_table.c.ante_id,
                             idea_evaluation_table.c.relatedness >= 3),
            secondaryjoin=(idea_evaluation_table.c.cons_id == idea_table.c.ID),
            order_by=idea_evaluation_table.c.relatedness.desc(),
            ),
        'related_thinkers':dynamic_loader(Thinker, secondary=idea_thinker_graph_edges_table,
            primaryjoin=and_(entity_table.c.ID ==idea_thinker_graph_edges_table.c.ante_id,
                             entity_table.c.typeID == 3),
            secondaryjoin=(idea_thinker_graph_edges_table.c.cons_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.jweight.desc(),
            ),
        'it_in_edges':dynamic_loader(IdeaThinkerGraphEdge, secondary=idea_thinker_graph_edges_table,
            primaryjoin=(entity_table.c.ID==idea_thinker_graph_edges_table.c.cons_id),
            secondaryjoin=(idea_thinker_graph_edges_table.c.cons_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.jweight.desc(),
            ),
        'it_out_edges':dynamic_loader(IdeaThinkerGraphEdge, secondary=idea_thinker_graph_edges_table,
            primaryjoin=(entity_table.c.ID==idea_thinker_graph_edges_table.c.ante_id),
            secondaryjoin=(idea_thinker_graph_edges_table.c.ante_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.jweight.desc(),
            ),
        'ii_in_edges':dynamic_loader(IdeaGraphEdge, secondary=idea_graph_edges_table,
            primaryjoin=(idea_table.c.ID==idea_graph_edges_table.c.cons_id),
            secondaryjoin=(idea_graph_edges_table.c.cons_id == idea_table.c.ID),
            order_by=idea_graph_edges_table.c.jweight.desc(),
            ),
        'ii_out_edges':dynamic_loader(IdeaGraphEdge, secondary=idea_graph_edges_table,
            primaryjoin=(idea_table.c.ID==idea_graph_edges_table.c.ante_id),
            secondaryjoin=(idea_graph_edges_table.c.ante_id == idea_table.c.ID),
            order_by=idea_graph_edges_table.c.jweight.desc(),
            ),
    })
    mapper(Node, ontotree_table, 
        inherits=Entity, polymorphic_identity=2, polymorphic_on=entity_table.c.typeID,
        properties={
        'children':relation(Node, lazy='joined', 
            primaryjoin=ontotree_table.c.ID==ontotree_table.c.parent_id,
            backref=backref('parent', remote_side=[ontotree_table.c.ID])), 
        'idea':relation(Idea, uselist=False, secondary=idea_table, lazy=False,
            primaryjoin=(idea_table.c.ID == ontotree_table.c.concept_id),
            secondaryjoin=(ontotree_table.c.concept_id == idea_table.c.ID),
            foreign_keys=[idea_table.c.ID]
            ), #uselist=False allows for 1:1 relation
    })
    mapper(Instance, idea_instance_of_table, properties={
        'class_idea':relation(Idea, uselist=False, secondary=idea_table,
            primaryjoin=(idea_table.c.ID == idea_instance_of_table.c.class_id),
            secondaryjoin=(idea_instance_of_table.c.class_id == idea_table.c.ID)
            ), #uselist=False allows for 1:1 relation
        'idea':relation(Idea, uselist=False, secondary=idea_table,
            primaryjoin=(idea_table.c.ID == idea_instance_of_table.c.instance_id),
            secondaryjoin=(idea_instance_of_table.c.instance_id == idea_table.c.ID)
            ), #uselist=False allows for 1:1 relation
    })
    mapper(IdeaEvaluation, idea_evaluation_table, properties={
        'ante':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
            primaryjoin=(idea_evaluation_table.c.ante_id == idea_table.c.ID),
            secondaryjoin=(idea_table.c.ID == idea_evaluation_table.c.ante_id)
            ), #uselist=False allows for 1:1 relation
        'cons':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
            primaryjoin=(idea_evaluation_table.c.cons_id == idea_table.c.ID),
            secondaryjoin=(idea_table.c.ID == idea_evaluation_table.c.cons_id)
            ), #uselist=False allows for 1:1 relation
        'user':relation(User, uselist=False, lazy=False, secondary=user_table,
            primaryjoin=(idea_evaluation_table.c.uid == user_table.c.ID),
            secondaryjoin=(user_table.c.ID == idea_evaluation_table.c.uid)
            )
    })
    mapper(AnonIdeaEvaluation, anon_evaluation_table, properties={
        'ante':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
            primaryjoin=(anon_evaluation_table.c.ante_id == idea_table.c.ID),
            secondaryjoin=(idea_table.c.ID == anon_evaluation_table.c.ante_id)
            ), #uselist=False allows for 1:1 relation
        'cons':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
            primaryjoin=(anon_evaluation_table.c.cons_id == idea_table.c.ID),
            secondaryjoin=(idea_table.c.ID == anon_evaluation_table.c.cons_id)
            ) #uselist=False allows for 1:1 relation
    })
    mapper(IdeaGraphEdge, idea_graph_edges_table, properties={
        'ante':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
            primaryjoin=(idea_graph_edges_table.c.ante_id == idea_table.c.ID),
            secondaryjoin=(idea_table.c.ID == idea_graph_edges_table.c.ante_id)
            ), #uselist=False allows for 1:1 relation
        'cons':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
            primaryjoin=(idea_graph_edges_table.c.cons_id == idea_table.c.ID),
            secondaryjoin=(idea_table.c.ID == idea_graph_edges_table.c.cons_id)
            ), #uselist=False allows for 1:1 relation


    })
    mapper(IdeaThinkerGraphEdge, idea_thinker_graph_edges_table, properties={
        'ante':relation(Entity, uselist=False, lazy=False, secondary=entity_table,
            primaryjoin=(idea_thinker_graph_edges_table.c.ante_id == entity_table.c.ID),
            secondaryjoin=(entity_table.c.ID == idea_thinker_graph_edges_table.c.ante_id)
            ), #uselist=False allows for 1:1 relation
        'cons':relation(Entity, uselist=False, lazy=False, secondary=entity_table,
            primaryjoin=(idea_thinker_graph_edges_table.c.cons_id == entity_table.c.ID),
            secondaryjoin=(entity_table.c.ID == idea_thinker_graph_edges_table.c.cons_id)
            ), #uselist=False allows for 1:1 relation


    })
    mapper(ThinkerGraphEdge, thinker_graph_edges_table, properties={
        'ante':relation(Thinker, uselist=False, lazy=False, secondary=thinker_table,
            primaryjoin=(thinker_graph_edges_table.c.ante_id == thinker_table.c.ID),
            secondaryjoin=(thinker_table.c.ID == thinker_graph_edges_table.c.ante_id)
            ), #uselist=False allows for 1:1 relation
        'cons':relation(Thinker, uselist=False, lazy=False, secondary=thinker_table,
            primaryjoin=(thinker_graph_edges_table.c.cons_id == thinker_table.c.ID),
            secondaryjoin=(thinker_table.c.ID == thinker_graph_edges_table.c.cons_id)
            ), #uselist=False allows for 1:1 relation


    })
    '''
    , properties={
    TODO : fix IdeaEvaluation Mapper
    'ante':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
        primaryjoin=(idea_table.c.ID == idea_evaluation_table.c.ante_id),
        secondaryjoin=(idea_evaluation_table.c.ante_id == idea_table.c.ID)
        ), #uselist=False allows for 1:1 relation
    'cons':relation(Idea, uselist=False, lazy=False, secondary=idea_table,
        primaryjoin=(idea_table.c.ID == idea_evaluation_table.c.cons_id),
        secondaryjoin=(idea_evaluation_table.c.cons_id == idea_table.c.ID)
        ), #uselist=False allows for 1:1 relation
    'user':relation(User, uselist=False, lazy=False, secondary=user_table,
        primaryjoin=(user_table.c.ID == idea_evaluation_table.c.uid),
        secondaryjoin=(idea_evaluation_table.c.uid == user_table.c.ID)
        ), #uselist=False allows for 1:1 relation
    }
    '''

    #define thinker mappings
    mapper(Thinker, thinker_table,
        inherits=Entity, polymorphic_identity=3, polymorphic_on=entity_table.c.typeID,
        properties={
        'nationalities':relation(Nationality, secondary=thinker_has_nationality_table),
        'professions':relation(Profession, secondary=thinker_has_profession_table),
        'influenced':relation(Thinker, secondary=thinker_has_influenced_evaluation_table,
            primaryjoin=(thinker_table.c.ID == thinker_has_influenced_evaluation_table.c.thinker1_id),
            secondaryjoin=(thinker_table.c.ID == thinker_has_influenced_evaluation_table.c.thinker2_id),
            cascade="all, delete",
            backref='influenced_by'),
        'students':relation(Thinker, secondary=thinker_teacher_of_evaluation_table,
            primaryjoin=(thinker_table.c.ID == thinker_teacher_of_evaluation_table.c.thinker1_id),
            secondaryjoin=(thinker_table.c.ID == thinker_teacher_of_evaluation_table.c.thinker2_id),
            cascade="all, delete",
            backref='teachers'),
        'occurrences':dynamic_loader(Thinker, secondary=thinker_graph_edges_table,
            primaryjoin=and_(thinker_table.c.ID == thinker_graph_edges_table.c.cons_id, 
                             thinker_graph_edges_table.c.occurs_in > 0),
            secondaryjoin=(thinker_graph_edges_table.c.ante_id == thinker_table.c.ID),
            order_by=thinker_graph_edges_table.c.occurs_in.desc(),
            ),
        'idea_occurrences':dynamic_loader(Idea, secondary=idea_thinker_graph_edges_table,
            primaryjoin=and_(entity_table.c.ID == idea_thinker_graph_edges_table.c.cons_id, 
                             idea_thinker_graph_edges_table.c.occurs_in > 0),
            secondaryjoin=(idea_thinker_graph_edges_table.c.ante_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.occurs_in.desc(),
            ),
        'hyponyms':dynamic_loader(Thinker, secondary=thinker_graph_edges_table,
            primaryjoin=and_(thinker_table.c.ID == thinker_graph_edges_table.c.cons_id, 
                             thinker_graph_edges_table.c.weight > 0),
            secondaryjoin=(thinker_graph_edges_table.c.ante_id == thinker_table.c.ID),
            order_by=thinker_graph_edges_table.c.weight.desc(),
            ),
        'related':dynamic_loader(Thinker, secondary=thinker_graph_edges_table,
            primaryjoin=(thinker_table.c.ID == thinker_graph_edges_table.c.ante_id),
            secondaryjoin=(thinker_graph_edges_table.c.cons_id == thinker_table.c.ID),
            order_by=thinker_graph_edges_table.c.jweight.desc(),
            ),
        'related_ideas':dynamic_loader(Idea, secondary=idea_thinker_graph_edges_table,
            primaryjoin=and_(entity_table.c.ID ==idea_thinker_graph_edges_table.c.ante_id,
                             entity_table.c.typeID == 1),
            secondaryjoin=(idea_thinker_graph_edges_table.c.cons_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.jweight.desc(),
            ),
        'hyponyms':dynamic_loader(Thinker, secondary=thinker_graph_edges_table,
            primaryjoin=and_(thinker_table.c.ID == thinker_graph_edges_table.c.cons_id, 
                             thinker_graph_edges_table.c.weight > 0),
            secondaryjoin=(thinker_graph_edges_table.c.ante_id == thinker_table.c.ID),
            order_by=thinker_graph_edges_table.c.weight.desc(),
            ),
        'related':dynamic_loader(Thinker, secondary=thinker_graph_edges_table,
            primaryjoin=(thinker_table.c.ID == thinker_graph_edges_table.c.ante_id),
            secondaryjoin=(thinker_graph_edges_table.c.cons_id == thinker_table.c.ID),
            order_by=thinker_graph_edges_table.c.jweight.desc(),
            ),
        'it_in_edges':dynamic_loader(IdeaThinkerGraphEdge, secondary=idea_thinker_graph_edges_table,
            primaryjoin=(entity_table.c.ID==idea_thinker_graph_edges_table.c.cons_id),
            secondaryjoin=(idea_thinker_graph_edges_table.c.cons_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.jweight.desc(),
            ),
        'it_out_edges':dynamic_loader(IdeaThinkerGraphEdge, secondary=idea_thinker_graph_edges_table,
            primaryjoin=(entity_table.c.ID==idea_thinker_graph_edges_table.c.ante_id),
            secondaryjoin=(idea_thinker_graph_edges_table.c.ante_id == entity_table.c.ID),
            order_by=idea_thinker_graph_edges_table.c.jweight.desc(),
            ),
        'tt_in_edges':dynamic_loader(ThinkerGraphEdge, secondary=thinker_graph_edges_table,
            primaryjoin=(thinker_table.c.ID==thinker_graph_edges_table.c.cons_id),
            secondaryjoin=(thinker_graph_edges_table.c.cons_id == thinker_table.c.ID),
            order_by=thinker_graph_edges_table.c.jweight.desc(),
            ),
        'tt_out_edges':dynamic_loader(ThinkerGraphEdge, secondary=thinker_graph_edges_table,
            primaryjoin=(thinker_table.c.ID==thinker_graph_edges_table.c.ante_id),
            secondaryjoin=(thinker_graph_edges_table.c.ante_id == thinker_table.c.ID),
            order_by=thinker_graph_edges_table.c.jweight.desc(),
            ),
    })
    """    'birth':composite(SplitDate, thinker_table.c.birth_year,
                                     thinker_table.c.birth_month,
                                     thinker_table.c.birth_day),
        'death':composite(SplitDate, thinker_table.c.death_year,
                                     thinker_table.c.death_month,
                                     thinker_table.c.death_day)"""

    mapper(Nationality, nationality_table)
    mapper(Profession, profession_table)
    mapper(Alias, alias_table)
    # TODO : Fix Thinker relation ORMs
    mapper(ThinkerTeacherEvaluation, thinker_teacher_of_evaluation_table, properties={
        '''
        'thinker1':relation(Thinker, uselist=False, secondary=thinker_table,
            primaryjoin=(thinker_table.c.ID == thinker_teacher_of_evaluation_table.c.thinker1_id),
            secondaryjoin=(thinker_table.c.ID == thinker_teacher_of_evaluation_table.c.thinker1_id),
        ),
        'thinker2':relation(Thinker, uselist=False, secondary=thinker_table,
            primaryjoin=(thinker_table.c.ID == thinker_teacher_of_evaluation_table.c.thinker2_id),
            secondaryjoin=(thinker_table.c.ID == thinker_teacher_of_evaluation_table.c.thinker2_id),
        ),
        '''
        'user':relation(User),
        'ante_id':thinker_teacher_of_evaluation_table.c.thinker1_id,
        'cons_id':thinker_teacher_of_evaluation_table.c.thinker2_id
        
    })
    mapper(ThinkerInfluencedEvaluation, thinker_has_influenced_evaluation_table, properties={
        '''
        'thinker1':relation(Thinker, uselist=False, secondary=thinker_table,
            primaryjoin=(thinker_table.c.ID == thinker_has_influenced_evaluation_table.c.thinker1_id),
            secondaryjoin=(thinker_table.c.ID == thinker_has_influenced_evaluation_table.c.thinker1_id),
        ),
        'thinker2':relation(Thinker, uselist=False, secondary=thinker_table,
            primaryjoin=(thinker_table.c.ID == thinker_has_influenced_evaluation_table.c.thinker2_id),
            secondaryjoin=(thinker_table.c.ID == thinker_has_influenced_evaluation_table.c.thinker2_id),
        ),
        '''
        'user':relation(User),
        'ante_id':thinker_has_influenced_evaluation_table.c.thinker1_id,
        'cons_id':thinker_has_influenced_evaluation_table.c.thinker2_id
    })
    

    # define Journal mappings
    mapper(Journal, journal_table,
        inherits=Entity, polymorphic_identity=4, polymorphic_on=entity_table.c.typeID,
        properties={
        'abbreviations':relation(Abbr),
        'query':relation(SearchQuery),
    })
    mapper(Abbr, journal_abbr_table)
    mapper(SearchQuery, journal_search_query_table)
    mapper(SearchPattern, searchpatterns_table)
    
    #Define works mappings
    mapper(Work, work_table, inherits=Entity, polymorphic_identity=5, polymorphic_on=entity_table.c.typeID)
    
    #Define SchoolOfThought mappings
    mapper(SchoolOfThought, school_of_thought_table, inherits=Entity, polymorphic_identity=6, polymorphic_on=entity_table.c.typeID)

    # define User mappings
    mapper(User, user_table, properties={
        'first_area':relation(Idea, uselist=False, secondary=idea_table,
            primaryjoin=(idea_table.c.ID == user_table.c.first_area_concept_id),
            secondaryjoin=(idea_table.c.ID == user_table.c.first_area_concept_id)
            ), #uselist=False allows for 1:1 relation
        'second_area':relation(Idea, uselist=False, secondary=idea_table,
            primaryjoin=(idea_table.c.ID == user_table.c.second_area_concept_id),
            secondaryjoin=(idea_table.c.ID == user_table.c.second_area_concept_id)
            ), #uselist=False allows for 1:1 relation
        "_roles": relation(Role, secondary=users_roles_table, lazy='immediate'),
        "group": relation(Group),
        "password": user_table.c.passwd
    })
    
    mapper(SEPArea, sep_area_table,properties={
        "idea": relation(Idea, uselist=False)
    })
    mapper(Group, groups_table,properties={
        "users": relation(User)
    })
    mapper(Role, roles_table,properties={
        "users": relation(User, secondary=users_roles_table)
    })
    
    mapper(SEPEntry, sepentries_table, properties={
            'fmatches':relation(Fuzzymatch,
            cascade="all, delete-orphan"),
    
    })
    
    mapper(Fuzzymatch, fuzzymatches_table)
    

