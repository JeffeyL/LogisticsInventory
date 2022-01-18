from flask import Response, request
from datetime import datetime
import json
from bson.objectid import ObjectId
from flaskinventory import db

class Item:

    def get(self):
        """
        Get a list of all inventory items
        """
        try:
            data = list(db.items.find())
            for item in data:
                item["_id"] = str(item["_id"])
            return Response(
                response = json.dumps(data),
                status=200,
                mimetype="application/json"
            )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"cannot read items"
                    }),
                status=500,
                mimetype="application/json"
            )
    
    def get_deleted(self):
        """
        Get a list of all temporarily deleted items
        """
        try:
            data = list(db.deleted_items.find())
            for item in data:
                item["_id"] = str(item["_id"])
            return Response(
                response = json.dumps(data),
                status=200,
                mimetype="application/json"
            )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"cannot read items"
                    }),
                status=500,
                mimetype="application/json"
            )

    def create(self, id, name, qty):
        """
        Create an item in the database

        Parameters
        id : str
            the item _id
        name : str
            the item name
        qty : str
            the item quantity
        """
        try:
            time = datetime.utcnow()    # Current UTC time (for consistency across timezones)
            item = {
                "id": id, 
                "name": name,
                "qty": qty,
                "last_update": time.strftime("%m/%d/%Y, %H:%M:%S")
                }
            dbResponse = db.items.insert_one(item)
            return Response(
                response=json.dumps({
                    "message":"successfully created item", 
                    "id":f"{dbResponse.inserted_id}"
                    }),
                status=200,
                mimetype="application/json"
            )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"unable to create item"
                    }),
                status=500,
                mimetype="application/json"
            )

    # Update the id of an item
    def update_id(self, id, newid, last_update):
        """
        Update the id of an item in the database

        Parameters
        id : str
            the item _id
        name : str
            the new id
        last_update : str
            The last time this item was updated
        """
        try:
            dbResponse = db.items.update_one(
                {"_id": ObjectId(id), "last_update": {"$eq": last_update}},
                {"$set": {"id": newid}}
            )
            if dbResponse.modified_count == 1:
                return Response(
                        response=json.dumps({
                            "message":"item id updated"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                return Response(
                        response=json.dumps({
                            "message":"nothing was updated"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"unable to update item"
                    }),
                status=500,
                mimetype="application/json"
            )
    
    def update_name(self, id, newname, last_update):
        """
        Update the name of an item in the database

        Parameters
        id : str
            the item _id
        name : str
            the new name
        last_update : str
            The last time this item was updated
        """
        try:
            time = datetime.utcnow()
            dbResponse = db.items.update_one(
                {"_id": ObjectId(id), "last_update": {"$eq": last_update}},
                {"$set": {"name": newname}}
            )
            if dbResponse.modified_count == 1:
                return Response(
                        response=json.dumps({
                            "message":"item name updated"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                return Response(
                        response=json.dumps({
                            "message":"nothing was updated"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"unable to update item"
                    }),
                status=500,
                mimetype="application/json"
            )

    def update_qty(self, id, newqty, last_update):
        """
        Update the quantity of an item in the database

        Parameters
        id : str
            the item _id
        newqty : str
            the new quantity
        last_update : str
            The last time this item was updated
        """
        try:
            dbResponse = db.items.update_one(
                {"_id": ObjectId(id), "last_update": {"$eq": last_update}},
                {"$set": {"qty": newqty}}
            )
            if dbResponse.modified_count == 1:
                return Response(
                        response=json.dumps({
                            "message":"item quantity updated"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                return Response(
                        response=json.dumps({
                            "message":"nothing was updated"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"unable to update item"
                    }),
                status=500,
                mimetype="application/json"
            )

    def delete(self, id, message):
        """
        Delete an item from the inventory and add it to
        the recently deleted items

        Parameters
        id : str
            the item _id
        message : str
            the delete message
        """
        try:
            time = datetime.utcnow()    # Current UTC time (for consistency across timezones)
            item = db.items.find_one({"_id": ObjectId(id)})
            db.deleted_items.insert_one(item)
            db.deleted_items.update_one({"_id": ObjectId(id)},
                                        {"$set": {"last_update": time.strftime("%m/%d/%Y, %H:%M:%S"),
                                         "msg": message}})
            dbResponse = db.items.delete_one(
                {"_id": ObjectId(id)},
            )
            if dbResponse.deleted_count == 1:
                return Response(
                        response=json.dumps({
                            "message":"item deleted",
                            "id":f"{id}"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                return Response(
                        response=json.dumps({
                            "message":"item not found",
                            "id":f"{id}"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"item deletion failed"
                    }),
                status=500,
                mimetype="application/json"
            )

    def delete_permanent(self, id):
        """
        Delete an item from the recently deleted items

        Parameters
        id : str
            the item _id
        """
        try:
            dbResponse = db.deleted_items.delete_one(
                {"_id": ObjectId(id)},
            )
            if dbResponse.deleted_count == 1:
                return Response(
                        response=json.dumps({
                            "message":"item permanently deleted",
                            "id":f"{id}"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                return Response(
                        response=json.dumps({
                            "message":"item not found",
                            "id":f"{id}"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"item deletion failed"
                    }),
                status=500,
                mimetype="application/json"
            )

    def restore(self, id):
        """
        Restore an item from recently deleted items to the inventory

        Parameters
        id : str
            the item _id
        """
        try:
            time = datetime.utcnow()    # Current UTC time (for consistency across timezones)
            item = db.deleted_items.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"last_update": time}})
            db.items.insert_one(item)
            dbResponse = db.deleted_items.delete_one(
                {"_id": ObjectId(id)},
            )
            if dbResponse.deleted_count == 1:
                return Response(
                        response=json.dumps({
                            "message":"item restored",
                            "id":f"{id}"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                return Response(
                        response=json.dumps({
                            "message":"item not found",
                            "id":f"{id}"
                            }),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message":"item deletion failed"
                    }),
                status=500,
                mimetype="application/json"
            )