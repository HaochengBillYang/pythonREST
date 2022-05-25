from flask import Blueprint, flash, redirect, render_template, request, url_for, session
import flask
import requests
from flask_login import login_required, current_user
from . import op

display = Blueprint('display', __name__)


@display.route('/', methods=['GET','POST'])
@login_required
def home():
    hosts = []
    if request.method == 'POST':
        port = request.form.get('port')
        url = request.form.get('url')
        session['port'] = port
        session['url'] = url
        return redirect(url_for("display.manage"))
        

    return render_template('home.html', user = current_user)

@display.route('/manage', methods=['GET','POST'])
@login_required
def manage():
    port = session['port']
    url = session['url']
    try:                            # Add loop to continuous get data
            key = op.get_token(url, port)
            session['clusters'] = []
            res1 = op.get_all_clusters(url,port,key)
            session['clusters'] = op.get_all_cluster_id_from_response(res1)
            for i in range(len(session['clusters'])):
                res2 = op.get_hosts_by_cluster_id(url,port,key,session['clusters'][i])
                host_temp = op.get_all_host_id_from_response(res2)
                session['hosts'] = [session['clusters'][i], host_temp]
                for j in range(len(session['hosts'][1])):
                    res3 = op.get_disks_by_host_id(url,port,key,session['hosts'][1][j])
                    disk_temp=op.get_all_disk_id_from_response(res3)
                    session['disks'] = [session['clusters'][i], session['hosts'][1][j], disk_temp]
                              # Print Operation

    except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
        flash("invalid url", type="error")               # Print Error Message

    return render_template('manage.html', user = current_user, disks = session['disks'], hosts = session['hosts'])
