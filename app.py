from flask import Flask
from pyVim.connect import SmartConnect,SmartConnectNoSSL 
from datetime import datetime, timedelta
from pyVmomi import vim
import ssl
import os
#import getpass
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Technical Computing Platform PoC'

@app.route('/hostConnection')
def hostConnectionPrint():
    return vcenter_connection()

@app.route('/dataStores')
def dataStoresPrint():
    return vcenter_health(os.environ['api_host'])


def vcenter_connection():
    return 'Printed host connections'

def vcenter_health(host):
    context = ssl._create_unverified_context()

    print("connecting with user:",os.environ['api_user'])
    si = SmartConnectNoSSL(host=host, user=os.environ['api_user'],
                              pwd=os.environ['api_pwd'])
    content=si.RetrieveContent()
    children = content.rootFolder.childEntity
    data = []
    
    for child in children:  # Iterate though DataCenters
        data.append(child)
    #data[0].child
    hosts=[]
    for host in data[0].childEntity:
        hosts.append(host)

    list=[]
    frontend={}
    for ds in hosts[1].datastore:

        if ("RGFX" in ds.name):
            frontend[ds.name]={}
            i=0
            for it in ds.vm:
                if (it.summary.runtime.powerState=="poweredOn"):
                   i=i+1
            list.append(i)
            frontend[ds.name]=i
    
    fe=dict(frontend)
    final_keys=[]
    final_values=[]
    final_numbers=[]
    for key in sorted(fe):
        final_keys.append(key)
        final_values.append(fe[key])
    final_dict=dict(zip(final_keys, final_values+ [None] * (len(final_keys) - len (final_values)) ))  
    frontend_html=pd.DataFrame(final_dict,["VMs"]).transpose().to_html()

    return frontend_html
    #return str(frontend)
    
    
# Start Flask Process
if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0', port=8080)#, ssl_context=context)#threaded=True)
#
# Rename App to Application for WSGI
application = app
