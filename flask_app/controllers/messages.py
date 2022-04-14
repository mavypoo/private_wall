from flask import render_template, session,flash,redirect, request
import re
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route("/create_message/", methods=["POST", "GET"])
def create_message():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "sender_id": request.form["sender_id"],
        "receiver_id": request.form["receiver_id"],
        "content": request.form["content"]
    }
    print(data)
    Message.save(data)
    return redirect("/dashboard/")


@app.route("/delete/<int:id>/message/")
def delete_message(id):
    data = {
        "id": id,
    }
    Message.delete(data)
    return redirect("/dashboard/")