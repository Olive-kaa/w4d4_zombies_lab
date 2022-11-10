from db.run_sql import run_sql
from models.human import Human
from models.zombie import Zombie
from models.biting import Biting

import repositories.zombie_repository as zombie_repository
import repositories.human_repository as human_repository

import pdb

# save
def save(biting):
    sql = """INSERT INTO bitings (human_id, zombie_id)
    VALUES (%s, %s) RETURNING id"""
    values = [biting.human.id, biting.zombie.id]
    results = run_sql(sql, values)
    # [ {"id": 41} ]
    id = results[0]['id']
    biting.id = id
    return biting

# select_all
def select_all():
    bitings = []
    sql = "SELECT * FROM bitings"
    results = run_sql(sql)

    for row in results:
        human = human_repository.select(row['human_id'])
        zombie = zombie_repository.select(row['zombie_id'])
        biting = Biting(human, zombie, row['id'])
        bitings.append(biting)
    return bitings

# select
def select(id):
    biting = None
    sql = "SELECT * FROM bitings WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        human = human_repository.select(result['human_id'])
        zombie = zombie_repository.select(result['zombie_id'])
        biting = Biting(human, zombie, result['id'])
    return biting

# delete
def delete(id):
    sql = "DELETE FROM bitings WHERE id = %s"
    values = [id]
    run_sql(sql, values)

# delete_all
def delete_all():
    sql = "DELETE FROM bitings"
    run_sql(sql)

# update
def update(biting):
    sql = "UPDATE bitings SET (human_id, zombie_id) = (%s, %s) WHERE id = %s"
    values = [biting.human.id, biting.zombie.id, biting.id]
    run_sql(sql,values)