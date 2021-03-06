import os
import re
import pydantic
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, jsonify, send_from_directory
import requests
from flask_login import login_required, current_user
from pydantic import BaseModel
from config.Config import ConnectionConfig
from config.ConfigManagement import remove_config_by_id, retrieve_config_by_type, save_config

from operation.disk.GiveDiskTagById import GiveDiskTagByIdOperation, GiveDiskTagByIdRequest
from operation.host.GetAllHost import GetAllHostOperation, GetAllHostRequest
from operation.disk.RemoveDiskTagById import RemoveDiskTagByIdOperation, RemoveDiskTagByIdRequest
from operation.cluster.CreateCluster import CreateClusterInfo, CreateClusterOperation, CreateClusterRequest
from config import *
from . import op
from .op import generate_list_on_cluster_to_str, generate_list_on_cluster, get_all_clusters
import os
from fastapi.encoders import jsonable_encoder

STATIC_FOLDER = os.getcwd() + "/webserver/static"

display = Blueprint("display", __name__)

import traceback


def exception_to_string(excp):
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
    pretty = traceback.format_list(stack)
    return '{} <br> {} '.format(excp.__class__, excp) + '<br>'.join(pretty) + '<br>'


@display.route("/", methods=["GET", "POST"])  # Say what method is allowed here
@login_required  # only users logged in are allowed
def home():
    configs = retrieve_config_by_type(uid=current_user.id, type=ConnectionConfig)
    if request.method == "POST":

        port = request.form.get("port")
        url = request.form.get("url")
        session["port"] = port  # session data--goes to any page
        session["url"] = url
        configs = retrieve_config_by_type(uid=current_user.id, type=ConnectionConfig)
        for config in configs:
            if config.host == url and config.port == int(port):
                remove_config_by_id(uid=current_user.id, config_id=config.config_id)

        save_config(current_user.id, ConnectionConfig(
            host=url,
            port=int(port)
        ))

        return redirect(url_for("display.manage"))
    configs = map(lambda x: x.dict(), configs)
    return render_template("home.html", user=current_user, config=configs)


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
    if request.method == "POST":
        name = request.form.get("name")
        minsize = request.form.get("size")
        copy = request.form.get("copy")
        ip = request.form.get("ip")
        CreateClusterOperation(
            host=url + ":" + port
        ).invoke(CreateClusterRequest(
            cluster=CreateClusterInfo(
                clusterName=name,
                minClusterSize=minsize,
                replicationFactor=copy,
                virtualIp=ip
            ),
            hosts=[]
        ))
    session['cluster'] = get_all_clusters(url, port)

    return render_template("manage.html", user=current_user, cluster=session['cluster'])


@display.route("/cluster", methods=["GET", "POST"])
@login_required
def cluster():
    if request.method == "GET":
        cluster_id = request.args.get('id', 'none', type=str)
        if cluster_id == 'none':
            return jsonify({"error": "id not found"})
        return send_from_directory(STATIC_FOLDER, STATIC_FOLDER, 'cluster.html')


def pack_exception(e: Exception):
    return jsonify({"success": False, "reason": exception_to_string(e)})


def pack_failure(e: Exception):
    return jsonify({"success": False, "reason": e})


def pack_success(e):
    return jsonable_encoder({"success": True, "data": e})


@display.route("/cluster/info", methods=["GET"])
@login_required
def cluster_info():
    cluster_id = request.args.get('id', 'none', type=str)
    if cluster_id == 'none':
        return jsonify({"error": "id not found"})
    try:
        return pack_success(generate_list_on_cluster(session["url"], session["port"], cluster_id))
    except Exception as e:
        return pack_exception(e)


@display.route("/cluster/host", methods=["GET"])
@login_required
def host_info():
    cluster_id = request.args.get('id', 'none', type=str)
    free = request.args.get('free', False, type=bool)
    if cluster_id == 'none':
        return jsonify({"error": "id not found"})
    try:
        server_host = session["url"] + ":" + str(session["port"])

        return pack_success(
            GetAllHostOperation(server_host).invoke(GetAllHostRequest(
                clusterId=cluster_id,
                onlyFreeHost=free
            )).data
        )
    except Exception as e:
        return pack_exception(e)


@display.route("/host/free", methods=["GET"])
@login_required
def host_free():
    try:
        server_host = session["url"] + ":" + str(session["port"])
        curr = []
        for host in GetAllHostOperation(server_host).invoke(GetAllHostRequest()).data:
            if host.clusterId is None:
                curr.append(host)

        pack_success(curr)

    except Exception as e:
        return pack_exception(e)


@display.route("cluster/disk/add-tag", methods=["POST"])
@login_required
def add_tag_request():
    fail = False
    failure_message = []
    tags = request.json['tags']
    for item in request.json['disks']:
        existing_tags = item['diskTags']
        tmp_all = tags + existing_tags
        all_tags = [];
        [all_tags.append(item) for item in tmp_all if item not in all_tags]
        a = 'DATA_DISK'
        b = 'METADATA_DISK'
        c = 'WRITE_CACHE'
        d = 'READ_CACHE'
        A = a in all_tags
        B = b in all_tags
        C = c in all_tags
        D = d in all_tags
        if not (not C and not D or not A and not B and not C or not A and not B and not C):
            fail = True
            failure_message.append(str(item['diskId']) + ' cannot be given tag: ' + str(tags) + '</br>')
    if fail:
        return pack_failure(''.join(failure_message))
    try:
        if fail == False:
            for item in request.json['disks']:
                for tag in tags:
                    GiveDiskTagByIdOperation(
                        host=(session['url'] + ':' + str(session['port']))
                    ).invoke(GiveDiskTagByIdRequest(
                        diskIds=[item['diskId']],
                        hostId=item['hostId'],
                        diskTag=tag
                    ))
                    # return a key task success?
                return pack_success("0 errors, 0 warnings")
    except Exception as e:
        return pack_exception(e)
    #    {'clusterId': 'd309fb6c-3115-4356-83d0-de23e9bc4071', 'tags': ['DATA_DISK'], 'disks': [
    #    {'diskId': '121cbcce-0784-4a6f-b556-41ea35ac218d', 'hostId': '00000000-0000-0000-0000-0CC47AD453B0',
    #    'diskTags': ['METADATA_DISK', 'DATA_DISK']},
    #    {'diskId': 'a0a96f62-60c8-4fd6-a684-50d246918b04', 'hostId': '00000000-0000-0000-0000-0CC47AD453B0',
    #    'diskTags': ['METADATA_DISK', 'DATA_DISK']}]}


@display.route("cluster/disk/remove-tag", methods=["POST"])
@login_required
def remove_tag_request():
    # {'clusterId': 'd309fb6c-3115-4356-83d0-de23e9bc4071', 'tags': ['DATA_DISK'], 'disks': [
    #    {'diskId': '121cbcce-0784-4a6f-b556-41ea35ac218d', 'hostId': '00000000-0000-0000-0000-0CC47AD453B0',
    ##     'diskTags': ['METADATA_DISK', 'DATA_DISK']},
    #    {'diskId': 'a0a96f62-60c8-4fd6-a684-50d246918b04', 'hostId': '00000000-0000-0000-0000-0CC47AD453B0',
    #    'diskTags': ['METADATA_DISK', 'DATA_DISK']}]}
    fail = False
    failure_message = []
    tags = request.json['tags']
    for item in request.json['disks']:
        existing_tags = item['diskTags']
        for tag in tags:
            if tag not in existing_tags:
                fail = True
                failure_message.append(str(item['diskId']) + ' cannot be deleted tag: ' + str(tags) + '</br>')

    if fail:
        return pack_failure(''.join(failure_message))
    try:
        if fail == False:
            for item in request.json['disks']:
                for tag in tags:
                    RemoveDiskTagByIdOperation(
                        host=(session['url'] + ':' + str(session['port']))
                    ).invoke(RemoveDiskTagByIdRequest(
                        diskIds=[item['diskId']],
                        hostId=item['hostId'],
                        diskTag=tag
                    ))
                    # return a key task success?
                return pack_success("0 errors, 0 warnings")
    except Exception as e:
        return pack_exception(e)

@display.route("log", methods=["GET"])
@login_required
def log():
    file = open("/home/hcd/Documents/webserverlog.txt", "r")
    content = file.read()
    content.replace("</p>", "")
    content = content.split('</br>')
    return render_template("log.html", user=current_user, log = content)

@display.route("/favicon.ico", methods=["GET"])
def icon():
    return send_from_directory(STATIC_FOLDER, STATIC_FOLDER, 'favicon.ico')
