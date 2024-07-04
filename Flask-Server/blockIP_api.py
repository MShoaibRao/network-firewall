

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import subprocess
# import sched
# import time
# from threading import Thread

# app = Flask(__name__)
# CORS(app)
# scheduler = sched.scheduler(time.time, time.sleep)

# block_data = {
#     'FACEBOOK': {
#         '01': {
#             'ips': [],
#             'domains': ['facebook.com', 'web.facebook.com']
#         },
#     },

#     'WHATSAPP': {
#         '02': {
#             'ips': [],
#             'domains': ['chat.cdn.whatsapp.net','www.whatsapp.com' 'whatsapp.com', 'web.whatsapp.com',
#                         'mmx-ds.cdn.whatsapp.net', 'scontent.whatsapp.net', 'dit.whatsapp.net',
#                         'chat.cdn.whatsapp.net', 'g.whatsapp.net', 'e1.wahstapp.net', 'e2.whatsapp.net',
#                         'e3.whatsapp.net', 'e4.whatsapp.net', 'e5.whatsapp.net', 'e6.whatsapp.net',
#                         'e7.whatsapp.net', 'e8.whatsapp.net', 'e9.whatsapp.net', 'e10.whatsapp.net',
#                         'e11.whatsapp.net', 'e12.whatsapp.net', 'e13.whatsapp.net', 'e14.whatsapp.net',
#                         'e15.whatsapp.net', 'e16.whatsapp.net']
#         },
#     },

#     'INSTAGRAM': {
#         '03': {
#             'ips': [],
#             'domains': ['instagram.com', 'i.instagram.com', 'graph.instagram.com',
#                         'd.ns.c10r.instagram.com', 'b.ns.c10r.instagram.com', 'c.ns.c10r.instagram.com',
#                         'a.ns.c10r.instagram.com', 'www.instagram.com', 'gateway.instagram.com',
#                         'instagram.c10r.instagram.com', 'instagram.fkhi22.fna.fbcdn.net']
#         },
#     },

#     # gmail
#     'GMAIL': {
#         '04': {
#             'ips': [],
#             'domains': ['gmail.com', 'mail.google.com', 'maps.google.com', 'inbox.google.com', 'mobile.webview.gmail.com', 'dial.meet.com', 'meet.google.com' , 'taskassist-pa.clients6.google.com',
#                         'enterprise.google.com', 't.meet.com', 'chat.google.com', 'd.meet.com',
#                         'tel.meet.com', 'gmail.app.goo.gl', 'dynamite-autopush.sandbox.google.com', 'peoplestack-pa.googleapis.com']
#         },
#     },

#     # PUBG
#     'PUBG': {
#         '05': {
#             'ips': [],
#             'domains': ['www.pubgmobile.com', 'pubgmobile.com']
#         },
#     },

#     # google
#     'GOOGLE': {
#         '06': {
#             'ips': ['142.250.0.0/15', '74.125.0.0/16', '142.250.153.0/24', '216.58.209.0/24', '172.217.18.0/24', '216.239.38.0/24'],
#             'domains': ['google.com', 'www.google.com']
#         },
#     },

#     # SNAPCHAT
#     'SNAPCHAT': {
#         '07': {
#             'ips': [],
#             'domains': ['www.snapchat.com', 'snapchat.com']
#         },
#     },

#     # Adult content
#     'ADULT CONTENT': {
#         '08': {
#             'ips': [],
#             'domains': ['www.pornhub.com', 'pornhub.com', 'www.xhamster.com', 'xhamster.com', 'www.xnxx.com', 'xnxx.com',
#                       'xvideos.com', 'www.xvideos.com' , 'www.bellesa.com', 'bellesa.com' ]
#         },
#     },




# }

# def block_ips_and_domains(ips, domains):
#     # Block IPs using iptables
#     # subprocess.run(['sudo', 'ufw', 'enable'])
#     for ip in ips:
#         subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])

#     # Block domains by adding them to /etc/hosts
#     with open('/etc/hosts', 'a') as hosts_file:
#         for domain in domains:
#             hosts_file.write(f"127.0.0.1 {domain}\n")

# def unblock_ips_and_domains(ips, domains):
#     # Unblock IPs using iptables
#     # subprocess.run(['sudo', 'ufw', 'disable'])
#     for ip in ips:
#         subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'])

#     # Unblock domains by removing them from /etc/hosts
#     with open('/etc/hosts', 'r') as hosts_file:
#         lines = hosts_file.readlines()
#     with open('/etc/hosts', 'w') as hosts_file:
#         for line in lines:
#             if not any(domain in line for domain in domains):
#                 hosts_file.write(line)

# def schedule_unblock(ips, domains, delay=300):
#     scheduler.enter(delay, 1, unblock_ips_and_domains, argument=(ips, domains))
#     thread = Thread(target=scheduler.run)
#     thread.start()

# @app.route('/api/block-ips', methods=['POST'])
# def block_ips():
#     data = request.get_json()
#     app_name = data.get('app')
#     id = data.get('id')

#     if app_name in block_data and id in block_data[app_name]:
#         ips = block_data[app_name][id]['ips']
#         domains = block_data[app_name][id]['domains']
        
#         block_ips_and_domains(ips, domains)
#         schedule_unblock(ips, domains)

#         return jsonify({'message': 'IPs and domains have been successfully blocked for 5 minutes'}), 200
#     else:
#         return jsonify({'error': 'Invalid id or app'}), 400

# if __name__ == '__main__':
#     app.run(port=5004)





















from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sched
import time
from threading import Thread

app = Flask(__name__)
CORS(app)
scheduler = sched.scheduler(time.time, time.sleep)

block_data = {
    'FACEBOOK': {
        '01': {
            'ips': [],
            'domains': ['facebook.com', 'web.facebook.com']
        },
    },
    'WHATSAPP': {
        '02': {
            'ips': [],
            'domains': ['chat.cdn.whatsapp.net', 'www.whatsapp.com', 'whatsapp.com', 'web.whatsapp.com',
                        'mmx-ds.cdn.whatsapp.net', 'scontent.whatsapp.net', 'dit.whatsapp.net',
                        'chat.cdn.whatsapp.net', 'g.whatsapp.net', 'e1.wahstapp.net', 'e2.whatsapp.net',
                        'e3.whatsapp.net', 'e4.whatsapp.net', 'e5.whatsapp.net', 'e6.whatsapp.net',
                        'e7.whatsapp.net', 'e8.whatsapp.net', 'e9.whatsapp.net', 'e10.whatsapp.net',
                        'e11.whatsapp.net', 'e12.whatsapp.net', 'e13.whatsapp.net', 'e14.whatsapp.net',
                        'e15.whatsapp.net', 'e16.whatsapp.net']
        },
    },
    'INSTAGRAM': {
        '03': {
            'ips': [],
            'domains': ['instagram.com', 'i.instagram.com', 'graph.instagram.com',
                        'd.ns.c10r.instagram.com', 'b.ns.c10r.instagram.com', 'c.ns.c10r.instagram.com',
                        'a.ns.c10r.instagram.com', 'www.instagram.com', 'gateway.instagram.com',
                        'instagram.c10r.instagram.com', 'instagram.fkhi22.fna.fbcdn.net']
        },
    },
    # gmail
    'GMAIL': {
        '04': {
            'ips': [],
            'domains': ['gmail.com', 'mail.google.com', 'maps.google.com', 'inbox.google.com', 'mobile.webview.gmail.com', 'dial.meet.com', 'meet.google.com', 'taskassist-pa.clients6.google.com',
                        'enterprise.google.com', 't.meet.com', 'chat.google.com', 'd.meet.com',
                        'tel.meet.com', 'gmail.app.goo.gl', 'dynamite-autopush.sandbox.google.com', 'peoplestack-pa.googleapis.com']
        },
    },
    # PUBG
    'PUBG': {
        '05': {
            'ips': [],
            'domains': ['www.pubgmobile.com', 'pubgmobile.com']
        },
    },
    # google
    'GOOGLE': {
        '06': {
            'ips': ['142.250.0.0/15', '74.125.0.0/16', '142.250.153.0/24', '216.58.209.0/24', '172.217.18.0/24', '216.239.38.0/24'],
            'domains': ['google.com', 'www.google.com']
        },
    },
    # SNAPCHAT
    'SNAPCHAT': {
        '07': {
            'ips': [],
            'domains': ['www.snapchat.com', 'snapchat.com']
        },
    },
    # Adult content
    'ADULT CONTENT': {
        '08': {
            'ips': [],
            'domains': ['www.pornhub.com', 'pornhub.com', 'www.xhamster.com', 'xhamster.com', 'www.xnxx.com', 'xnxx.com',
                      'xvideos.com', 'www.xvideos.com', 'www.bellesa.com', 'bellesa.com']
        },
    },
}

# Track the block state
block_state = {}

def block_ips_and_domains(ips, domains):
    # Block IPs using iptables
    for ip in ips:
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])

    # Block domains by adding them to /etc/hosts
    with open('/etc/hosts', 'a') as hosts_file:
        for domain in domains:
            hosts_file.write(f"127.0.0.1 {domain}\n")

def unblock_ips_and_domains(ips, domains):
    # Unblock IPs using iptables
    for ip in ips:
        subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'])

    # Unblock domains by removing them from /etc/hosts
    with open('/etc/hosts', 'r') as hosts_file:
        lines = hosts_file.readlines()
    with open('/etc/hosts', 'w') as hosts_file:
        for line in lines:
            if not any(domain in line for domain in domains):
                hosts_file.write(line)

def check_ip_block(ip):
    result = subprocess.run(['sudo', 'iptables', '-L', 'INPUT', '-v', '-n'], stdout=subprocess.PIPE)
    return ip in result.stdout.decode()

@app.route('/api/toggle-block', methods=['POST'])
def toggle_block():
    data = request.get_json()
    app_name = data.get('app')
    id = data.get('id')

    if app_name in block_data and id in block_data[app_name]:
        ips = block_data[app_name][id]['ips']
        domains = block_data[app_name][id]['domains']
        
        if block_state.get((app_name, id), False):
            unblock_ips_and_domains(ips, domains)
            block_state[(app_name, id)] = False
            message = 'IPs and domains have been successfully unblocked'
        else:
            block_ips_and_domains(ips, domains)
            block_state[(app_name, id)] = True
            message = 'IPs and domains have been successfully blocked'

        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': 'Invalid id or app'}), 400

@app.route('/api/check-block', methods=['POST'])
def check_block():
    data = request.get_json()
    ip = data.get('ip')
    if ip:
        is_blocked = check_ip_block(ip)
        return jsonify({'ip': ip, 'blocked': is_blocked}), 200
    else:
        return jsonify({'error': 'IP address is required'}), 400

if __name__ == '__main__':
    app.run(port=5004)



