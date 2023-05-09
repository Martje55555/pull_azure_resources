from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

all_subs = pd.read_csv('list_of_all_subscriptions.csv')
db_df = pd.DataFrame(columns=['Resource ID', 'Sku_Name', 'Capacity', 'Edition'])

credential = AzureCliCredential()

for i in range(len(all_subs)):
    subscription_id = all_subs['sub_id'][i]

    try:
        resource_mgmt_client = ResourceManagementClient(credential, subscription_id)

        resource_group_list = resource_mgmt_client.resource_groups.list()

        resource_list = resource_mgmt_client.resources.list()

        for resource in resource_list:
            if "Microsoft.Sql/servers/databases" in resource.type:
                try:
                    print(resource.sku)
                    db_df = db_df.append({
                        'Resource ID': resource.id,
                        'Sku_Name': resource.sku.name,
                        'Capacity': resource.sku.capacity,
                        'Edition': resource.sku.tier
                        }, ignore_index=True)
                except:
                    print(i)
    except:
        print('unable to read subscription: ' + subscription_id)
        
print('done')
db_df.to_csv('example_temporary.csv',index=False)