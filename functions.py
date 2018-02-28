#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import http.cookiejar as HC
import json
from functools import wraps

def base_func(func):
    @wraps(func)
    def wrapper(*args, **kw):
        #check whether the user have login
        if (not os.path.exists('/tmp/cookies/cookie.txt')) or (not os.path.exists('/tmp/cookies/baseurl')) \
                or (not os.path.exists('/tmp/cookies/masterIP')):
            print('please login first!')
            print('run docklet login -h for help')
            exit(1)
        #load cookie and set session
        load_cookiejar = HC.LWPCookieJar()
        load_cookiejar.load('/tmp/cookies/cookie.txt', ignore_discard=True, ignore_expires=True)
        load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
        conect_s = requests.Session()
        conect_s.cookies = requests.utils.cookiejar_from_dict(load_cookies)
        #get base_url
        f = open('/tmp/cookies/baseurl')
        baseurl = f.read()
        f.close()
        f = open('/tmp/cookies/masterIP')
        masterIP = f.read()
        f.close()
        return func(conect_s,baseurl,masterIP,*args, **kw)
    return wrapper


def login(args):
    #check whether there is already one user
    if os.path.exists('/tmp/cookies/cookie.txt') or os.path.exists('/tmp/cookies/baseurl') or os.path.exists('/tmp/cookies/masterIP'):
        print("Error: there is already one user, if you want to use another account ,please logout first!")
        exit(0)
    #create session
    conect_s=requests.Session()
    #get url
    baseurl = 'http://' + args.address
    login_url=baseurl+'/login/'
    payload = {
        "username": args.username,
        "password": args.password
    }
    #send requests and handle response
    response = conect_s.post(url=login_url, data=payload)
    if 'workspace' in response.text:
        print('login to %s success' % [args.address])
    else:
        print('login to %s fail,please check your command and try again' % [args.address])
        exit(1)
    #store base_url and masterIP to local
    f = open('/tmp/cookies/baseurl', 'w')
    f.write(baseurl)
    f.close()
    f = open('/tmp/cookies/masterIP', 'w')
    f.write(args.masterIP)
    f.close()
    #store cookie to local
    new_cookie_jar = HC.LWPCookieJar('cookie.txt')
    requests.utils.cookiejar_from_dict({c.name: c.value for c in conect_s.cookies}, new_cookie_jar)
    new_cookie_jar.save('/tmp/cookies/cookie.txt', ignore_discard=True, ignore_expires=True)

@base_func
def beans_apply(conect_s,baseurl,masterIP,args):
    #get url
    apply_beans_url = baseurl + "/beans/apply/"
    payload = {
        "number": args.num,
        "reason": args.reason,
        "remlen": 300 - len(args.reason)
    }
    # send requests and handle response
    response = conect_s.post(url=apply_beans_url, data=payload)
    if response.status_code==requests.codes.ok:
        print("apply beans, request sent success")
    else:
        print("apply beans, request sent failed")

@base_func
def logout(conect_s,baseurl,masterIP,args):
    # get url
    logout_url = baseurl + '/logout/'
    # send requests and handle response
    response = conect_s.get(url=logout_url)
    if os.path.exists('/tmp/cookies/baseurl'):
        os.remove('/tmp/cookies/baseurl')
    if os.path.exists('/tmp/cookies/cookie.txt'):
        os.remove('/tmp/cookies/cookie.txt')
    if os.path.exists('/tmp/cookies/masterIP'):
        os.remove('/tmp/cookies/masterIP')
    print('logout success')

@base_func
def workspace_add(conect_s,baseurl,masterIP,args):
    #get url
    workspacce_add_url = baseurl + '/workspace/'+masterIP+'/add/'
    payload = {
        "clusterName": args.name,
        "image": args.image,
        "cpuSetting": args.c,
        "memorySetting": args.m,
        "diskSetting": args.d
    }
    # send requests and handle response
    response = conect_s.post(url=workspacce_add_url, data=payload)
    if response.status_code==requests.codes.ok:
        print('create workspace %s, request sent success' % args.name)
    else:
        print('create workspace %s, request sent failed' % args.name)

@base_func
def workspace_start(conect_s,baseurl,masterIP,args):
    #get url
    workspace_start_url = baseurl + "/workspace/"+masterIP+"/start/" + args.name + "/"
    # send requests and handle response
    response = conect_s.get(url=workspace_start_url)
    if response.status_code==requests.codes.ok:
        print('start workspace %s, request sent success' % args.name)
    else:
        print('start workspace %s, request sent failed' % args.name)

@base_func
def workspace_stop(conect_s,baseurl,masterIP,args):
    #get url
    workspace_stop_url = baseurl + "/workspace/"+masterIP+"/stop/" + args.name + "/"
    # send requests and handle response
    response = conect_s.get(url=workspace_stop_url)
    if response.status_code==requests.codes.ok:
        print('stop workspace %s, request sent success' % args.name)
    else:
        print('stop workspace %s, request sent failed' % args.name)

@base_func
def workspace_delete(conect_s,baseurl,masterIP,args):
    #get url
    workspace_delete_url = baseurl + "/workspace/"+masterIP+"/delete/" + args.name + "/"
    # send requests and handle response
    response = conect_s.get(url=workspace_delete_url)
    if response.status_code==requests.codes.ok:
        print('delete workspace %s, request sent success' % args.name)
    else:
        print('delete workspace %s, request sent failed' % args.name)

@base_func
def node_add(conect_s,baseurl,masterIP,args):
    #get url
    node_add_url = baseurl + "/workspace/"+masterIP+"/scaleout/" + args.w_name + "/"
    payload = {
        "DataTables_Table_0_length": args.dt_len,
        "image": args.image,
        "cpuSetting": args.c,
        "memorySetting": args.m,
        "diskSetting": args.d
    }
    # send requests and handle response
    response = conect_s.post(url=node_add_url, data=payload)
    if response.status_code==requests.codes.ok:
        print('add node to workspace %s, request sent success' % args.w_name)
    else:
        print('add node to workspace %s, request sent failed' % args.w_name)

@base_func
def node_default_set(conect_s,baseurl,masterIP,args):
    #get url
    node_default_set_url = baseurl + '/quota/chlxcsetting/'
    payload = {
        "lxcCpu": args.cpu_num,
        "lxcMemory": args.memory_size,
        "lxcDisk": args.disk_size
    }
    # send requests and handle response
    response = conect_s.post(url=node_default_set_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('set node default config, request sent success')
    else:
        print('set node default config, request sent failed')

@base_func
def node_delete(conect_s,baseurl,masterIP,args):
    #get url
    node_delete_url = baseurl + "/workspace/"+masterIP+"/scalein/" + args.w_name + "/" + args.n_name + "/"
    # send requests and handle response
    response = conect_s.get(url=node_delete_url)
    if response.status_code==requests.codes.ok:
        print('delete node %s from workspace %s, request sent success' % (args.n_name,args.w_name))
    else:
        print('delete node %s from workspace %s, request sent failed' % (args.n_name,args.w_name))

@base_func
def node_save(conect_s,baseurl,masterIP,args):
    #get url
    save_image_url = baseurl + "/workspace/"+masterIP+"/save/" + args.w_name + "/" + args.n_name + "/"
    payload = {
        'ImageName': args.i_name,
        'description': args.description
    }
    # send requests and handle response
    response = conect_s.post(url=save_image_url, data=payload)
    if response.status_code==requests.codes.ok:
        print('save node %s from workspace %s as image %s, request sent success' % (args.n_name,args.w_name,args.i_name))
    else:
        print('save node %s from workspace %s as image %s, request sent failed' % (args.n_name,args.w_name,args.i_name))

@base_func
def port_apply(conect_s,baseurl,masterIP,args):
    #get url
    apply_port_url = baseurl + '/port_mapping/add/'+masterIP+'/'
    payload = {
        "clustername": args.w_name,
        "node_name": args.n_name,
        "node_ip": args.node_ip,
        "node_port": args.port
    }
    # send requests and handle response
    response = conect_s.post(url=apply_port_url, data=payload)
    if response.status_code==requests.codes.ok:
        print('apply port for node %s of workspace %s, request sent success' % (args.n_name,args.w_name))
    else:
        print('apply port for node %s of workspace %s, request sent failed' % (args.n_name,args.w_name))

@base_func
def port_delete(conect_s,baseurl,masterIP,args):
    # get url
    port_delete_url = baseurl + '/port_mapping/delete/'+masterIP+'/' + args.w_name + '/' + args.n_name + '/'+args.port+'/'
    # send requests and handle response
    response = conect_s.get(url=port_delete_url)
    if response.status_code==requests.codes.ok:
        print('delete port for node %s of workspace %s, request sent success' % (args.n_name,args.w_name))
    else:
        print('delete port for node %s of workspace %s, request sent failed' % (args.n_name,args.w_name))

@base_func
def group_add(conect_s,baseurl,masterIP,args):
    #get url
    group_add_url = baseurl + '/group/add/'
    payload = {
        "groupname": args.name,
        "cpu": args.cpu_num,
        "memory": args.memory_size,
        "disk": args.disk_size,
        "data": args.data_size,
        "image": args.image_num,
        "idletime": args.idletime,
        "vnode": args.vnode_num
    }
    # send requests and handle response
    response = conect_s.post(url=group_add_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('add group %s, request sent success' % args.name)
    else:
        print('add group %s, request sent failed' % args.name)

@base_func
def group_edit(conect_s,baseurl,masterIP,args):
    #get url
    group_edit_url = baseurl + "/group/modify/" + args.name + "/"
    payload = {
        "groupname": args.name,
        "cpu": args.cpu_num,
        "memory": args.memory_size,
        "disk": args.disk_size,
        "data": args.data_size,
        "image": args.image_num,
        "idletime": args.idletime,
        "vnode": args.vnode_num
    }
    # send requests and handle response
    response = conect_s.post(url=group_edit_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('change config of group %s, request sent success' % args.name)
    else:
        print('change config of group %s, request sent failed' % args.name)

@base_func
def group_delete(conect_s,baseurl,masterIP,args):
    #get url
    group_delete_url = baseurl + "/group/delete/" + args.name + "/"
    # send requests and handle response
    response = conect_s.get(url=group_delete_url)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('delete group %s, request sent success' % args.name)
    else:
        print('delete group %s, request sent failed' % args.name)

@base_func
def notification_add(conect_s,baseurl,masterIP,args):
    #get url
    notification_add_url = baseurl + '/notification/create/'
    payload = {
        "title": args.title,
        "content": args.content,
        "groups": args.groups
    }
    # send requests and handle response
    response = conect_s.post(url=notification_add_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('add notification %s, request sent success' % args.title)
    else:
        print('add notification %s, request sent failed' % args.title)

@base_func
def notification_edit(conect_s,baseurl,masterIP,args):
    #get url
    notification_edit_url = baseurl + '/notification/modify/'
    payload = {
        "title": args.title,
        "content": args.content,
        "notify_id": args.notify_id,
        "groups": args.groups,
        "status": args.status

    }
    # send requests and handle response
    response = conect_s.post(url=notification_edit_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('change set of notification %s, request sent success' % args.title)
    else:
        print('change set of notification %s, request sent failed' % args.title)

@base_func
def notification_delete(conect_s,baseurl,masterIP,args):
    #get url
    notification_delete_url = baseurl + '/notification/delete/'
    payload = {
        "notify_id": args.notify_id
    }
    # send requests and handle response
    response = conect_s.post(url=notification_delete_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('delete notification %s, request sent success' % args.notify_id)
    else:
        print('delete notification %s, request sent failed' % args.notify_id)

@base_func
def user_add(conect_s,baseurl,masterIP,args):
    #get url
    user_add_url = baseurl + '/user/add/'
    payload = {
        "username": args.name,
        "password": args.password,
        "e_mail": args.e_mail
    }
    # send requests and handle response
    response = conect_s.post(url=user_add_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('add user %s, request sent success' % args.name)
    else:
        print('add user %s, request sent failed' % args.name)

@base_func
def user_edit(conect_s,baseurl,masterIP,args):
    #get url
    user_edit_url = baseurl + '/user/modify/'
    payload = {
        "username": args.name,
        "status": args.status,
        "truename": args.truename,
        "e_mail": args.e_mail,
        "department": args.department,
        "student_number": args.student_num,
        "tel": args.tel,
        "group": args.group,
        "auth_method": args.auth_method,
        "description": args.description
    }
    # send requests and handle response
    response = conect_s.post(url=user_edit_url, data=payload)
    if 'Sorry, but you did not have the authorizaion for that action' in response.text:
        print('Error! only administrator can do this!')
    elif response.status_code==requests.codes.ok:
        print('change user info of %s, request sent success' % args.name)
    else:
        print('change user info of %s, request sent failed' % args.name)