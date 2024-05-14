import requests
import json
import base64
import pprint
import os
from dotenv import load_dotenv

load_dotenv()


class Moysklad:
    def __init__(self):
        self.login = os.getenv('MOYSKLAD_LOGIN')
        self.password = os.getenv('MOYSKLAD_PASSWORD')
        self.base_url = 'https://api.moysklad.ru/api/remap/1.2/'
        self.token_headers = self.get_token_header()
        self.access_token = self.get_access_token()
        self.main_headers = self.headers('Bearer', self.access_token)

    @staticmethod
    def headers(auth_type, auth_data):
        return {
            'Authorization': f'{auth_type} {auth_data}',
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip'
        }

    def get_token_header(self):
        auth_type = 'Basic'
        auth_data = f'{self.login}:{self.password}'
        auth_data = auth_data.encode('utf-8')
        auth_data = base64.b64encode(auth_data)
        auth_data = auth_data.decode('utf-8')
        return auth_type, auth_data

    def get_access_token(self):
        auth_type, auth_data = self.get_token_header()
        self.token_headers = self.headers(auth_type, auth_data)
        response = requests.post(self.base_url + 'security/token', headers=self.headers(auth_type, auth_data), data={}
                                 ).json()
        print(response)
        return response['access_token']

    def get(self, url, params=None):
        response = requests.get(self.base_url + url, headers=self.main_headers, params=params)
        return response.json()

    def post(self, url, data):
        response = requests.post(self.base_url + url, headers=self.main_headers, data=json.dumps(data))
        return response.json()

    def put(self, url, data):
        response = requests.put(self.base_url + url, headers=self.main_headers, data=json.dumps(data))
        return response.json()

    def delete(self, url):
        response = requests.delete(self.base_url + url, headers=self.main_headers)
        return response.json()

    def get_retaildemand(self, retaiddemand_id: str):
        return self.get(f'entity/retaildemand/{retaiddemand_id}')

    def get_counterparty(self, counterparty_id: str):
        return self.get(f'entity/counterparty/{counterparty_id}')

    def get_countreparty_tags(self, counterparty_id: str):
        return self.get_counterparty(counterparty_id)['tags']

    def get_positions(self, retaildemand_id: str):
        return self.get(f'entity/retaildemand/{retaildemand_id}/positions')

    def get_position_products_array(self, retaildemand_id: str):
        positions = self.get_positions(retaildemand_id)
        result = []
        for position in positions['rows']:
            total_price = position['price'] * position['quantity']
            if 'discount' in position:
                total_price = total_price - (total_price / 100 * position['discount'])
            result.append({'product_link': position['assortment']['meta']['href'], 'total_price': total_price,
                           'type': position['assortment']['meta']['type']})
        print(result)
        return result

    def get_products_cashback_array(self, retaildemand_id: str):
        products_array = self.get_position_products_array(retaildemand_id)
        products_cashback = []
        for product in products_array:
            if product['type'] == 'service':
                product_obj = self.service(product['product_link'].split('/')[-1])
            else:
                product_obj = self.get_product(product['product_link'].split('/')[-1])
            attributes = product_obj['attributes'] if 'attributes' in product_obj else []
            percent_cashback = 0
            for attribute in attributes:
                if attribute['name'] == '% Cashback':
                    percent_cashback = attribute['value']
            if percent_cashback > 0:
                total_cashback_sum = product['total_price'] * percent_cashback / 100
                products_cashback.append(total_cashback_sum)
        if products_cashback:
            pprint.pprint("Сума кешбеку")
            pprint.pprint(sum(products_cashback))
            return round(sum(products_cashback) / 100, 2)

        return products_cashback

    def get_product(self, product_id: str):
        return self.get(f'entity/product/{product_id}')

    def service(self, service_id: str):
        return self.get(f'entity/service/{service_id}')

    def edit_retaildemand_description(self, retaildemand_id: str):
        old_description = ''
        if 'description' in self.get_retaildemand(retaildemand_id):
            old_description = self.get_retaildemand(retaildemand_id)['description']
        new_description = f'{old_description} Cashback: {self.get_products_cashback_array(retaildemand_id)}'
        response = self.put(f'entity/retaildemand/{retaildemand_id}', {'description': new_description})
        return response
