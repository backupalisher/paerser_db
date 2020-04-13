from db import db


def insert_brand(brand):
    q = db.i_request(f'WITH s as (SELECT id FROM brands '
                     f'WHERE LOWER(name) = LOWER(\'{brand}\')), i as '
                     f'(INSERT INTO brands (name) SELECT \'{brand}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')


def insert_model(model, brand_id):
    q = db.i_request(f'WITH s as (SELECT id FROM models '
                     f'WHERE LOWER(name) = LOWER(\'{model}\')), i as '
                     f'(INSERT INTO models (name, brand_id) SELECT \'{model}\', \'{brand_id}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
    return q[0][0]


def insert_spr_details(model):
    q = db.i_request(f'WITH s as (SELECT id FROM spr_details '
                     f'WHERE LOWER(name) = LOWER(\'{model}\')), i as '
                     f'(INSERT INTO spr_details (name) SELECT \'{model}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s')
    return q[0][0]
