from urllib.parse import urlencode
import requests
import json
import time

def find_items(**kwargs):
    
    payload = { 'OPERATION-NAME' : 'findItemsAdvanced',
               'SERVICE-VERSION' : '1.13.0',
               'SECURITY-APPNAME' : 'StefanoR-ebayFric-PRD-19f17700d-ff298548',
               'RESPONSE-DATA-FORMAT' : 'JSON',
               'GLOBAL-ID' : 'EBAY-US',
               'REST-PAYLOAD' : '',
               'paginationInput.entriesPerPage' : 100 }
    
    i = 0
    
    if 'sellerId' in kwargs.keys():
        payload['itemFilter({}).name'.format(i)] = 'Seller'
        payload['itemFilter({}).value'.format(i)] = kwargs['sellerId']
        i += 1
        
    if 'keywords' in kwargs.keys():
        payload['keywords'] = kwargs['keywords']
        
    if 'site' in kwargs.keys():
        payload['GLOBAL-ID'] = kwargs['global_id']

    if 'page_nr' in kwargs.keys():
        payload['paginationInput.pageNumber'] = kwargs['page_nr']
        
    if 'app_key' in kwargs.keys():
        payload['SECURITY-APPNAME'] = kwargs['app_key']
    
    url_templ = "https://svcs.ebay.com/services/search/FindingService/v1?"

    results = { 'tot_pages' : 0,
                'page_nr' : 0,
                'tot_results' : 0,
                'items' : [],
                'status' : 'Success',
                'error_msg' : '' }
        
    url = url_templ + urlencode(payload)
    r = requests.get(url)
    j = json.loads(r.text)
    
    if 'findItemsAdvancedResponse' in j.keys():
        
        if j['findItemsAdvancedResponse'][0]['ack'][0] == 'Success':
            if results['tot_pages'] == 0:
                msg = "Zero items found with this search query"
                results['error_msg'] = msg
        
        elif j['findItemsAdvancedResponse'][0]['ack'][0] in ['Warning', 'PartialFailure']:
            results['status'] = j['findItemsAdvancedResponse'][0]['ack'][0]
            results['error_msg'] = j['findItemsAdvancedResponse'][0]['errorMessage'][0]['error'][0]['message'][0]
        
        elif j['findItemsAdvancedResponse'][0]['ack'][0] == 'Failure':
            msg = j['findItemsAdvancedResponse'][0]['errorMessage'][0]['error'][0]['message'][0]
            raise Exception(msg)
    
    elif 'errorMessage' in j.keys():
        msg = j['errorMessage'][0]['error'][0]['message'][0]
        raise Exception(msg)
        
    elif 'errors' in j.keys():
        msg = j['errors'][0]['longMessage']
        raise Exception(msg)
    
    else:
        raise Exception(json.dumps(j))

    results['tot_pages'] = int(j['findItemsAdvancedResponse'][0]['paginationOutput'][0]['totalPages'][0])
    results['page_nr'] = int(j['findItemsAdvancedResponse'][0]['paginationOutput'][0]['pageNumber'][0])
    results['tot_results'] = int(j['findItemsAdvancedResponse'][0]['paginationOutput'][0]['totalEntries'][0])

    for item in j['findItemsAdvancedResponse'][0]['searchResult'][0]['item']:
        results['items'].append(item['itemId'][0])
    
    # pausing 110 milliseconds to space queries to avoid more than 10 calls per second.
    time.sleep(0.11)
    return results
        
        
def find_items_mult_pages(**kwargs):
    
    page_nr = 1
    
    results_list = []
    
    tot_pages = 0
    
    while True:
        
        try:
            results = find_items(**kwargs)
        except Exception as e:
            msg = e.args[0]
            p = kwargs['page_nr']
            t = tot_pages
            k = kwargs['keywords']
            params = "page {} of {}, search \"{}\"".format(p, t, k)
            error = "{}\n{}".format(params , msg)
            raise Exception(error)
        else:
            results_list.append(results)
            
            tot_pages = results['tot_pages']
            
            if results['page_nr'] == 100:
                break
            elif results['page_nr'] == results['tot_pages']:
                break
            else:
                kwargs['page_nr'] = results['page_nr'] + 1
    
    return results_list


def find_items_mult_sites(**kwargs):
    
    results_list = []
    
    if len(kwargs['sites']) == 0:
        kwargs['sites'].append('US')
        
    for site in kwargs['sites']:
        global_id = globalSiteMap[site]['globalID']
        
        kwargs['global_id'] = global_id
        
        results = find_items_mult_pages(**kwargs)
        
        results_list.extend(results)
        
    return results_list


def items_description(list_of_items, site_id = 0):
    
    if len(list_of_items) > 20:
        raise Exception("Too many items. Provide a list of no more than 20!")
        
    items_string = ','.join(list_of_items)
        
    url_templ = "http://open.api.ebay.com/shopping?"

    payload = { 'appid' : 'StefanoR-ebayFric-PRD-19f17700d-ff298548',
                'callname' : 'GetMultipleItems',
                'version' : '975',
                'responseencoding' : 'JSON',
                'ItemID' : items_string,
                'IncludeSelector' : 'Details',
                'siteid' : site_id }

    url = url_templ + urlencode(payload)
    r = requests.get(url)
    j = json.loads(r.text)
    if j['Ack'] != 'Success':
        ack = j['Ack']
        msg = j['Errors'][0]['LongMessage']
        error = "Ack {}: {}".format(ack, msg)
        raise Exception(error)
    
    # pausing 110 milliseconds to space queries to avoid more than 10 calls per second.
    time.sleep(0.11)
    return j['Item']


def multi_items_description(list_of_items, site_id = 0):
    
    # split nr of item in single request if > 20 per request
    max_items = 20
    items_matrix = [ list_of_items[ i : i + max_items ] for i in range(0, len(list_of_items), max_items ) ]

    results = []
    
    for items_list in items_matrix:
        
        items = items_description(items_list, site_id)

        results.extend(items)

    return results


searches = ['tommy hilfiger shirt', 'polo ralph lauren', 'baby oil']
for search in searches:

    j = find_items_mult_pages(site = 'EBAY-GB', keywords = search)
    items_list = []
    for r in j:
        for item in r['items']:
            if item not in items_list:
                items_list.append(item)

    print("found {} unique results, for {}".format(len(items_list), search))

    j = multi_items_description(items_list, site_id = 3)

    print("returned {} item descriptions for {}".format(len(j), search))
