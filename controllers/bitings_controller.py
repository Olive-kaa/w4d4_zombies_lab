from flask import Blueprint, Flask, redirect, render_template, request

bitings_blueprint = Blueprint("bitings", __name__)

from repositories import human_repository, zombie_repository, biting_repository

from models.human import Human
from models.zombie import Zombie
from models.biting import Biting

import pdb


# INDEX
@bitings_blueprint.route("/bitings")
def bitings():
    bitings = biting_repository.select_all()
    humans = human_repository.select_all()
    zombies = zombie_repository.select_all()
    return render_template("/bitings/index.html", all_bitings = bitings, all_humans = humans, all_zombies = zombies)

# NEW
@bitings_blueprint.route("/bitings/new")
def new_biting():
    humans = human_repository.select_all()
    zombies = zombie_repository.select_all()
    return render_template("bitings/new.html", all_humans = humans, all_zombies = zombies)

# CREATE
@bitings_blueprint.route("/bitings", methods=["POST"])
def create_biting():
    input_human = request.form['human_id']
    input_zombie = request.form['zombie_id']
    selected_human = human_repository.select(input_human)
    selected_zombie = zombie_repository.select(input_zombie)
    new_biting = Biting(selected_human, selected_zombie)
    biting_repository.save(new_biting)
    return redirect('/bitings')

# EDIT
@bitings_blueprint.route('/bitings/<id>/edit')
def edit_biting(id):
    biting = biting_repository.select(id)
    humans = human_repository.select_all()
    zombies = zombie_repository.select_all()
    return render_template('/bitings/edit.html', biting = biting, all_humans = humans, all_zombies = zombies)

# UPDATE
@bitings_blueprint.route('/bitings/<id>', methods = ["POST"])
def update_biting(id):
    input_human = request.form['human_id']
    input_zombie = request.form['zombie_id']
    selected_human = human_repository.select(input_human)
    selected_zombie = zombie_repository.select(input_zombie)
    biting = Biting(selected_human, selected_zombie, id)
    biting_repository.update(biting)
    return redirect("/bitings")


# DELETE
@bitings_blueprint.route('/bitings/<id>/delete', methods=["POST"])
def delete_biting(id):
    biting_repository.delete(id)
    return redirect("/bitings")
