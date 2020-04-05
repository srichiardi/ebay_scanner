from modules.ebayAppWidgets import appDlg
from ebay_api import *

# options = appDlg().mainloop()
# 
# for key in options.keys():
#     print(key)
#     print(options[key])
    
searches = ['tommy hilfiger shirt', 'polo ralph lauren', 'baby oil']

options = {'outputFolder' : 'C:/Users/srichiardi/Documents/Project_Files/ebay_app',
'sites' : ['BE-FR', 'GB', 'IT', 'PL', 'US'],
'sellerId' : None,
'descriptionSearch' : 'false',
'keywords' : 'tommy hilfiger shirt'}

results_by_site = find_items_mult_sites(**options)