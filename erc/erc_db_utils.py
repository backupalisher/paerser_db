from db import db


def insert_error_code(code):
    q = db.i_request(f'WITH s as (SELECT id FROM error_code WHERE code = \'{code}\'), '
                     f'i as (INSERT INTO error_code (code) SELECT \'{code}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) returning id) SELECT id FROM i UNION ALL SELECT id FROM s')

    return q[0][0]


def update_code_display(erc_code_id, value):
    db.i_request(f'UPDATE error_code SET display = \'{value}\' WHERE id = {erc_code_id}')


def update_code(erc_code_id, name, value):
    db.i_request(f'UPDATE error_code SET {name} = \'{value}\' WHERE id = {erc_code_id}')


# перед тем как добавить проверяем на дубликаты
def insert_spr_error_code(spr_table, name, param):
    q = db.i_request(f'WITH s as (SELECT id FROM {spr_table} WHERE '
                     f'{name} = \'{param}\'), i as (INSERT INTO {spr_table} ({name}) SELECT \'{param}\' '
                     f'WHERE NOT EXISTS (SELECT 1 FROM s) returning id) SELECT id FROM i UNION ALL SELECT id FROM s')

    return q[0][0]


# def insert_spr_error_code(spr_table, name, param):
#     q = db.i_request(f'INSERT INTO {spr_table} ({name}) VALUE (\'{param}\') RETURNING id '
#
#     return q[0][0]


def insert_link_model_error_code(model_id, error_code_id):
    db.i_request(f'WITH s as (SELECT 1 FROM link_model_error_code '
                 f'WHERE model_id = {model_id} AND error_code_id = {error_code_id}), i as '
                 f'(INSERT INTO link_model_error_code (model_id, error_code_id) '
                 f'SELECT {model_id}, {error_code_id} WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING 0) '
                 f'SELECT * FROM i UNION ALL SELECT * FROM s')
