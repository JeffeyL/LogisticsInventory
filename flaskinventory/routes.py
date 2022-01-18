from flask.helpers import url_for
from flaskinventory import app, db
from flask import render_template, redirect, make_response, request
from flaskinventory.forms import CreateItemForm, UpdateItemForm, DeleteItemForm, GetUserForm
from flaskinventory.models.itemmodel import Item
from bson.objectid import ObjectId
from datetime import datetime

##################################################
# web display routes
##################################################

@app.route("/", methods=['GET', 'POST'])
def landing():
    form = GetUserForm()
    if form.validate_on_submit():
        user = form.username.data
        items = Item().get()
        items = items.json
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('userID', user)
        return resp
    return render_template('landing.html', form=form)

@app.route("/home")
def home():
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    items = Item().get()
    items = items.json
    return render_template('home.html', items=items)

@app.route("/deleted")
def deleted():
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    items = Item().get_deleted()
    items = items.json
    return render_template('deleted.html', items=items)

##################################################
# Item routes
##################################################

@app.route("/items", methods=["GET"])
def get_item():
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    return Item().get()

@app.route("/items/new", methods=['GET', 'POST'])
def new_item():
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    form = CreateItemForm()
    print(form.data)
    if form.validate_on_submit():
        Item().create(form.id.data, form.name.data, form.qty.data)
        return redirect(url_for("home"))
    return render_template('create_item.html', form=form, legend='New Item')

@app.route("/items/update/<id>", methods=['GET', 'PATCH', 'POST'])
def update_item(id):
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    form = UpdateItemForm()
    item = db.items.find_one({"_id": ObjectId(id)})
    lastupdate = item["last_update"]
    print(form.data)
    if form.validate_on_submit():
        if form.id.data != "":
            Item().update_id(id, form.id.data, lastupdate)
        if form.name.data != "":
            Item().update_name(id, form.name.data, lastupdate)
        if form.qty.data != "":
            Item().update_qty(id, form.qty.data, lastupdate)
        db.items.update_one(
                {"_id": ObjectId(id), "last_update": {"$eq": lastupdate}},
                {"$set": {"last_update": datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")}}
            )
        return redirect(url_for('home'))
    return render_template('update_item.html', item=item,
                        form=form, legend='Update Item (leave blank for no change)')

@app.route("/items/delete/<id>", methods=['GET', 'DELETE', 'POST'])
def delete_item(id):
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    form = DeleteItemForm()
    if form.validate_on_submit():
        Item().delete(id, form.message.data)
        return redirect(url_for('deleted'))
    return render_template('delete_item.html', form=form,
                            legend='Delete Item')

##################################################
# Deleted Item routes
##################################################

@app.route("/items/restore/<id>", methods=['GET', 'DELETE', 'PATCH'])
def restore_item(id):
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    Item().restore(id)
    return redirect(url_for('home'))

@app.route("/items/permdelete/<id>", methods=['GET', 'DELETE'])
def perm_delete_item(id):
    username = request.cookies.get('userID')
    if username is None:
        return redirect(url_for('landing'))
    Item().delete_permanent(id)
    return redirect(url_for('deleted'))
