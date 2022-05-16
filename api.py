import requests
import json

url="https://metabase.munitienda.com/public/question/e8e1234f-6818-430f-a6c8-86585cd4ef09.json"
response = requests.get(url)
if  response.status_code == 200:
    content = response.json()
    i=0
    for row in content:
        routeName= row['routeName']
        FUName=row['FUName']
        Service_Zone=row['Service_Zone']
        fk_order= row['fk_order']
        packer=row['packer']
        FuOrder=row['FuOrder']
        ean=row['ean']
        operationGroup=row['operationGroup']
        productName=row['productName']
        type=row['type']
        deliveryDate=row['deliveryDate']
        originalQuantity=row['originalQuantity']
        Vendor=row['Vendor']
        CLid=row['CLid']
        Stop=row['Stop']
        currentQuantity=row['currentQuantity']
        pendingQuantity=originalQuantity-currentQuantity
        if originalQuantity <= currentQuantity :
            Status= 'Finished'
        else:
            Status= 'Pendding'
        i=i+1
        print(i)





