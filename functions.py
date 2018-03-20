#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from functools import wraps

#set config
try:
    with open("./config.json",'r') as load_f:
        load_dict = json.load(load_f)
        user_port=load_dict['USER_PORT']
        host_ip=load_dict['MASTER_IP']
        master_port=load_dict['MASTER_PORT']
except FileNotFoundError:
    msg = "sorry, config file does not exist."
    print(msg)
    exit(1)

def base_func(func):
    @wraps(func)
    def wrapper(*args, **kw):
        #check whether the user have login
        if not os.path.exists('./.docklet-cookies/token.json'):
            print('please login first!')
            print('run docklet login -h for help')
            exit(1)
        #load token
        try:
            cookie_file=open('./.docklet-cookies/token.json','r')
        except:
            print('fail to open the token file')
            exit(1)
        cookie=json.load(cookie_file)
        cookie_file.close()

        return func(cookie,*args, **kw)
    return wrapper

def login(args):
    # check whether there is already one user
    if os.path.exists('./.docklet-cookies/token.json'):
        print("Error: there is already one user, if you want to use another account ,please logout first!")
        exit(1)
    # get url
    baseurl = 'http://' + host_ip+':'+user_port
    login_url = baseurl + '/login/'
    payload = {
        "user": args.user,
        "key": args.password
    }
    # send requests and handle response
    try:
        result = requests.post(url=login_url, data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('login success')
        if not os.path.exists('./.docklet-cookies/'):
            os.makedirs('./.docklet-cookies/')
        f=open("./.docklet-cookies/token.json", "w")
        json.dump(result, f)
        f.close()
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def logout(cookie,args):
    if os.path.exists('./.docklet-cookies/token.json'):
        os.remove('./.docklet-cookies/token.json')
    #if os.path.exists('./.docklet-cookies/master_ip'):
    #    os.remove('./.docklet-cookies/master_ip')
    print('logout success')
    exit(0)

@base_func
def image_list(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/image/list/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        for group in result['images']:
            print('%s :' % group)
            if group=='private':
                for image in result['images'][group]:
                    print(image)
            elif group=='public':
                for image in result['images'][group]:
                    print('%s : %s' % (image,result['images'][group][image]))
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def image_share(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "image": args.name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/image/share/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success share image')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def image_unshare(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "image": args.name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/image/unshare/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success unshare image')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def image_delete(cookie,  args):
    payload = {
        'token': cookie['data']['token'],
        "image": args.name
    }
    try:
        result = requests.post(url='http://'+host_ip+':'+master_port + '/image/delete/', data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success'] == 'true':
        print('success delete image')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def image_updatebase(cookie,  args):
    payload = {
        'token': cookie['data']['token'],
        "image": args.name
    }
    try:
        result = requests.post(url='http://'+host_ip+':'+master_port + '/image/updatebase/', data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success'] == 'true':
        print('success update base image')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def cluster_create(cookie,args):
    index1 = args.image.rindex("_")
    index2 = args.image[:index1].rindex("_")
    payload={
        'token':cookie['data']['token'],
        "clustername": args.name,
        "imagename": args.image[:index2],
        "imageowner":args.image[index2+1:index1],
        "imagetype":args.image[index1+1:],
        "cpuSetting": args.c,
        "memorySetting": args.m,
        "diskSetting": args.d
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/create/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success create cluster')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def cluster_start(cookie,args):
    payload={
        "clustername": args.name,
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/start/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success start workspace %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def cluster_stop(cookie,args):
    payload = {
        "clustername": args.name,
        'token': cookie['data']['token']
    }
    try:
        result = requests.post(url='http://'+host_ip+':'+master_port + '/cluster/stop/', data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success'] == 'true':
        print('success stop workspace %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def cluster_delete(cookie,args):
    payload = {
        "clustername": args.name,
        'token': cookie['data']['token']
    }
    try:
        result = requests.post(url='http://'+host_ip+':'+master_port + '/cluster/delete/', data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success'] == 'true':
        print('success delete workspace %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def cluster_list(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/list/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        for each_cluster in result['clusters']:
            print(each_cluster)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def cluster_info(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "clustername": args.name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/info/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        for (key,value) in sorted(result['message'].items()):
            print(key,value)
        exit(0)
    else:
        print(result['message'])
        exit(1)


@base_func
def node_add(cookie,args):
    index1 = args.image.rindex("_")
    index2 = args.image[:index1].rindex("_")
    payload = {
        'token': cookie['data']['token'],
        "clustername": args.w_name,
        "imagename": args.image[:index2],
        "imageowner": args.image[index2 + 1:index1],
        "imagetype": args.image[index1 + 1:],
        "cpuSetting": args.c,
        "memorySetting": args.m,
        "diskSetting": args.d
    }
    try:
        result = requests.post(url='http://'+host_ip+':'+master_port + '/cluster/scaleout/', data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success'] == 'true':
        print('success add node to %s' % args.w_name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def node_delete(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "containername": args.n_name,
        "clustername": args.w_name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/scalein/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true' or result['message']=='No port mapping.':
        print('success delete node %s' % args.n_name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def node_save(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "clustername": args.w_name,
        "image": args.i_name,
        "containername": args.n_name,
        "description": args.description,
        "isforce": args.isforce
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/save/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print(result)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def node_flush(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "clustername": args.w_name,
        "from_lxc": args.n_name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/flush/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success flush node %s' % args.n_name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def node_list(cookie,args):
    payload = {
        'token': cookie['data']['token'],
        "clustername": args.name
    }
    try:
        result = requests.post(url='http://'+host_ip+':'+master_port + '/cluster/info/', data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success'] == 'true':
        for x in result['message']['containers']:
            for (key,value) in sorted(x.items()):
                print(key,value)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def node_status(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/monitor/vnodes/%s/basic_info/'%(args.n_name),data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        for (key,value) in sorted(result['monitor']['basic_info'].items()):
            print(key,value)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def node_default_set(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "lxcCpu": args.cpu_num,
        "lxcMemory": args.memory_size,
        "lxcDisk": args.disk_size
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/chlxcsetting/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success set default config for node')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def node_default_get(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/lxcsettingList/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print(result['data'])
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def status_all(cookie,args):
    payload = {
        'token': cookie['data']['token']
    }
    try:
        result = requests.post(url='http://'+host_ip+':'+master_port + '/cluster/list/', data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success'] == 'true':
        for cluster in result['clusters']:
            cluster_payload={
                'token': cookie['data']['token'],
                "clustername": cluster
            }
            try:
                cluster_result = requests.post(url='http://'+host_ip+':'+master_port + '/cluster/info/', data=cluster_payload).json()
            except:
                print('fail to send the request,check your connection')
                exit(1)
            if cluster_result['success'] == 'true':
                for container in cluster_result['message']['containers']:
                    container_payload = {
                        'token': cookie['data']['token']
                    }
                    try:
                        container_result=requests.post(url='http://'+host_ip+':'+master_port+'/monitor/vnodes/%s/basic_info/'%(container['containername']),data=container_payload).json()
                    except:
                        print('fail to send the request,check your connection')
                        exit(1)
                    if container_result['success'] == 'true':
                        for (key,value) in sorted(container_result['monitor']['basic_info'].items()):
                            print(key,value)
                    else:
                        print(container_result['message'])
                        exit(1)
            else:
                print(cluster_result['message'])
                exit(1)
        exit(0)

@base_func
def port_apply(cookie,args):
    payload={
        'token': cookie['data']['token'],
        "clustername": args.w_name
    }
    containers=requests.post(url='http://'+host_ip+':'+master_port+'/cluster/info/',data=payload).json()['message']['containers']
    node_ip='0'
    for container in containers:
        if container['containername']==args.n_name:
            node_ip=container['ip'][:-3]
    payload = {
        'token': cookie['data']['token'],
        'clustername':args.w_name,
        'node_name':args.n_name,
        'node_ip':node_ip,
        'node_port':args.port
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/port_mapping/add/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success add port_mapping')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def port_delete(cookie,args):
    payload={
        'token':cookie['data']['token'],
        'clustername':args.w_name,
        'node_name':args.n_name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/port_mapping/delete/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success delete port_mapping')
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def history(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/monitor/user/createdvnodes/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print(result.get('createdvnodes'))
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def beans_apply(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "number": args.num,
        "reason": args.reason
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/beans/apply/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    print(result['message'])
    exit(0)

@base_func
def logs_list(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/logs/list/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print(result['result'])
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def log_get(cookie,args):
    payload={
        'token':cookie['data']['token'],
        'filename':args.name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/logs/get/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print(result)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def user_list(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/data/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print(result['data'])
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def user_add(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "username": args.name,
        "password": args.password,
        "e_mail": args.e_mail
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/add/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success add user %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(0)

@base_func
def user_edit(cookie,args):
    payload={
        'token':cookie['data']['token'],
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
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/modify/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success update info of user %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def user_default(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+master_port+'/monitor/user/quotainfo/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print(result['quotainfo'])
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def group_list(cookie,args):
    payload={
        'token':cookie['data']['token']
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/groupList/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        for group in result['groups']:
            print(group)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def group_add(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "groupname": args.name,
        "cpu": args.cpu_num,
        "memory": args.memory_size,
        "disk": args.disk_size,
        "data": args.data_size,
        "image": args.image_num,
        "idletime": args.idletime,
        "vnode": args.vnode_num
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/groupadd/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success add group %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def group_edit(cookie,args):
    payload={
        'token':cookie['data']['token'],
        "groupname": args.name,
        "cpu": args.cpu_num,
        "memory": args.memory_size,
        "disk": args.disk_size,
        "data": args.data_size,
        "image": args.image_num,
        "idletime": args.idletime,
        "vnode": args.vnode_num
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/groupModify/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success update group %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

@base_func
def group_delete(cookie,args):
    payload={
        'token':cookie['data']['token'],
        'name':args.name
    }
    try:
        result=requests.post(url='http://'+host_ip+':'+user_port+'/user/groupdel/',data=payload).json()
    except:
        print('fail to send the request,check your connection')
        exit(1)
    if result['success']=='true':
        print('success delete group %s' % args.name)
        exit(0)
    else:
        print(result['message'])
        exit(1)

