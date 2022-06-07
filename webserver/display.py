from flask import Blueprint, flash, redirect, render_template, request, url_for, session
import requests
from flask_login import login_required, current_user
from . import op
from .op import generate_list_on_cluster_to_str, generate_list_on_cluster, get_all_clusters

display = Blueprint("display", __name__)


@display.route("/", methods=["GET", "POST"])  # Say what method is allowed here
@login_required  # only users logged in are allowed
def home():
    if request.method == "POST":
        port = request.form.get("port")
        url = request.form.get("url")
        session["port"] = port  # session data--goes to any page
        session["url"] = url
        return redirect(url_for("display.manage"))

    return render_template("home.html", user=current_user)


# Say what method is allowed here
@display.route("/disk", methods=["GET", "POST"])
@login_required
def disk():
    port = session["port"]
    url = session["url"]
    try:
        session["disk_list"] = op.generate_list(url, port)
        # Data structure is [disk, host, cluster], [disk, host, cluster]

    except requests.exceptions.MissingSchema:  # Invalid URL will throw this exception
        flash("invalid url", type="error")  # Print Error Message

    if request.method == "POST":
        operation = request.form.get("submit_button")
        machines = []
        targets = []
        for disk in session["disk_list"]:
            machines.append(request.form.get(disk[0]))
        n = 0
        for machine in machines:
            if machine is not None:
                targets.append(session["disk_list"][n])
            n += 1

        success = 1
        for item in targets:
            if operation == "1":  # Give and Enable Tags
                log1 = op.give_disk_tag_by_id(
                    url, port, item, tag="DATA_DISK")
                log2 = op.give_disk_tag_by_id(
                    url, port, item, tag="METADATA_DISK")
                # op.give_disk_tag_by_id(url, port, key, item, tag="READ_CACHE")
                # op.give_disk_tag_by_id(url, port, key, item, tag="WRITE_CACHE")
                if log1.ok and log2.ok:
                    pass
                else:
                    success = 0
                    flash(log1.json(), category="error")
                    flash(log2.json(), category="error")
            elif operation == "2":  # Delete and Disable Tags
                log1 = op.remove_datadisk_tag_by_id(
                    url, port, item, tag="DATA_DISK")
                log2 = op.remove_datadisk_tag_by_id(
                    url, port, item, tag="METADATA_DISK")
                if log1.ok and log2.ok:
                    pass
                else:
                    success = 0
                    flash(log1.json(), category="error")
                    flash(log2.json(), category="error")
        if success:
            flash("OK")

    return render_template("disk.html", user=current_user, disks=session["disk_list"],
                           cluster_id='d309fb6c-3115-4356-83d0-de23e9bc4071',
                           render_data=generate_list_on_cluster(session["url"], session["port"],
                                                                       'd309fb6c-3115-4356-83d0-de23e9bc4071'))
                           # type: dict[str, (str, list[dict[str, any]])]

@display.route("/user", methods=["GET", "POST"])
@login_required
def user():
    flash("user page reached")
    return render_template("user.html", user=current_user)


@display.route("/volume", methods=["GET", "POST"])
@login_required
def volume():
    flash("volume page reached")
    return render_template("volume.html", user=current_user)


@display.route("/manage", methods=["GET", "POST"])
@login_required
def manage():
    port = session["port"]
    url = session["url"]
    session['cluster'] = get_all_clusters(url, port)
    return render_template("manage.html", user=current_user, cluster = session['cluster'])
