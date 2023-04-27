import requests
from bs4 import BeautifulSoup
import sys
import manage_db as db_con
from datetime import datetime
url = "https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx"

def store_deals_info(value_dct):
    try:
        db_connection = db_con.connection_pool()
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO deals (deal_date, security_code, security_name, client_name, deal_type, quantity, price, datamode, created_on,updated_on) VALUES ('{deal_date}', '{security_code}', '{security_name}', '{client_name}', '{deal_type}', '{quantity}', '{price}', 'active', NOW(), NOW());".format(
            deal_date = datetime(2009,5,5),
            security_code=value_dct['security_code'],
            security_name=value_dct['security_name'],
            client_name=value_dct['client_name'],
            deal_type=value_dct['deal_type'],
            quantity=value_dct['quantity'],
            price=value_dct['price'])
        res = cursor.execute(insert_query)
        db_connection.commit()
        db_connection.close()
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in extract_deals_detail function at %s:%s' % (exc_traceback.tb_lineno, e))       

def extract_deals_detail():
    try:
        response = requests.get(url,headers={'User-Agent': 'Custom'})
        soup = BeautifulSoup(response.text)
        values = []
        table = soup.find('table', attrs={'id': 'ContentPlaceHolder1_gvbulk_deals'})
        keys = ['deal_date','security_code','security_name','client_name','deal_type','quantity','price']
        for row in table.findAll("tr"):
            in_values = {}
            cnt =0
            for rw in row.findAll("td"):
                in_values[str(keys[cnt])] = rw.get_text()
                cnt +=1
            if len(in_values) > 1:
                deal_date = in_values['deal_date']
                deal_date_lst = deal_date.split('/')
                deal_date = datetime(year=int(deal_date_lst[2]),month=int(deal_date_lst[1]),day=int(deal_date_lst[0])),
                in_values['deal_date'] = deal_date
                store_deals_info(in_values)
                values.append(in_values)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in extract_deals_detail function at %s:%s' % (exc_traceback.tb_lineno, e))       



extract_deals_detail()