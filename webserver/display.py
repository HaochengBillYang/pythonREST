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
            session['all_disks'] = []
            session['clusters'] = []
            session['disks'] = []
            session['hosts'] = []
            res1 = op.get_all_clusters(url,port,key)
            session['clusters'] = op.get_all_cluster_id_from_response(res1)
            for i in range(len(session['clusters'])):
                res2 = op.get_hosts_by_cluster_id(url,port,key,session['clusters'][i])
                host_temp = op.get_all_host_id_from_response(res2)
                session['hosts'].append([session['clusters'][i], host_temp])
                for j in range(len(session['hosts'][i][1])):
                    res3 = op.get_disks_by_host_id(url,port,key,session['hosts'][i][1][j])
                    disk_temp=op.get_all_disk_id_from_response(res3)
                    all_info = res3.json()
                    session['disks'].append([session['clusters'][i], session['hosts'][i][1][j], disk_temp, all_info])
                    for disk in disk_temp:
                        session['all_disks'].append(disk)
                        tmp = []
                        [tmp.append(x) for x in session['all_disks'] if x not in tmp]
                        session['all_disks'] = tmp
                              # Print Operation
    
    except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
        flash("invalid url", type="error")               # Print Error Message
        
    if request.method == 'POST':
        operation = request.form.get("submit_button")
        machines = []
        disk_list = []
        for disks in session["disks"]:
            for element in disks[2]:
                machines.append(request.form.get(element))
        #flash(session['all_disks'])
        n = 0
        for machine in machines:
            
            if machine is not None:
                disk_list.append(session['all_disks'][n])
            n+=1

        for item in disk_list:
            if operation == '1':
                flash('Tags DATADISK, METADATADISK given to disk: ' + str(item))
            elif operation == 2:
                pass
            elif operation ==3:
                pass
            elif operation ==4:
                pass


        
                
        #flash(operation)
        #flash(disk_list)


    return render_template('manage.html', user = current_user, disks = session['disks'], hosts = session['hosts'])

