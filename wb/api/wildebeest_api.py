import urllib3
import json
import shutil
import os
import requests
import sys

class WildebeestApi(object):
    __version__ = '1.0.1'
    server_url = ''

    def __init__(self):
        self.server_url = os.environ.get('WB_SERVER_URL', 'http://183.111.79.18')

    def organizations_list_cli(self):
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/organization_list' % self.server_url)
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            if body['success']:
                print(' %-20s %-30s %10s' % ('NAME', 'DISPLAY NAME', 'DATASETS'))
                for i in body['result']:
                    r = http.request('GET', '%s/api/3/action/organization_show?id=%s' % (self.server_url, i))
                    if r.status == 200:
                        body = json.loads(r.data.decode('utf-8'))
                        if body['success']:
                            print(' %-20s %-30s %10d' % (i, body['result']['display_name'], body['result']['package_count']))

    def organizations_show_cli(self, organization_id):
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/organization_show?id=%s' % (self.server_url, organization_id))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            print(json.dumps(body, sort_keys=True, indent=4))
        else:
            print('status=', r.status)

    def organizations_datasets_cli(self, organization_id, page):
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/package_search?q=organization:%s&rows=20&start=%d' %
                         (self.server_url, organization_id, (int(page)-1) * 20))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            if body['success']:
                result = body['result']
                print(' Found: %d' % result.get('count'))
                print('%38s %-75s %9s' % ('ID', 'TITLE', 'RESOURCES'))
                if 'results' in result.keys():
                    for dataset in result['results']:
                        print(' %36s %-80s %4d' % (dataset['id'], dataset['title'][:100], dataset['num_resources']))


    def datasets_list_cli(self, page=1):
        print('dataset list')
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/package_list?limit=20&offset=%d' % (self.server_url, (int(page)-1) * 20))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            if body['success']:
                print('%38s %-75s %9s' % ('ID', 'TITLE', 'RESOURCES'))
                for i in body['result']:
                    r = http.request('GET', '%s/api/3/action/package_show?id=%s' % (self.server_url, i))
                    if r.status == 200:
                        body = json.loads(r.data.decode('utf-8'))
                        if body['success']:
                            print('%38s %-80s %4d' % (i, body['result']['title'][:100], body['result']['num_resources']))

    def datasets_show_cli(self, dataset_id):
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/package_show?id=%s' % (self.server_url, dataset_id))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            print(json.dumps(body, sort_keys=True, indent=4))
        else:
            print('status=', r.status)

    def datasets_search_cli(self, query='', page=1):
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/package_search?q=%s&rows=20&start=%d' % (self.server_url, query, (int(page)-1) * 20))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            if body['success']:
                result = body['result']
                print(' Found: %d' % result.get('count'))
                print(' %36s %-75s %9s' % ('ID', 'TITLE', 'RESOURCES'))
                for result in result['results']:
                    print(' %36s %-80s %4d' % (result['id'], result['title'][:100], result['num_resources']))

    def datasets_resources_cli(self, dataset=''):
        if dataset is None:
            print('dataset id is required!')
            return

        print('dataset resources', dataset)
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/package_show?id=%s' % (self.server_url, dataset))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            if body['success'] and body['result']['num_resources'] > 0:
                print('%38s %100s %10s %5s' % ('ID', 'NAME', 'FORMAT', 'DS'))
                for i in body['result']['resources']:
                    print('%38s %100s %10s %5s' % (i['id'], i['name'], i['format'][:100], i['datastore_active']))

    def datasets_download_cli(self, dataset_id):
        if dataset_id is None:
            print('dataset id is required!')
            return

        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/package_show?id=%s' % (self.server_url, dataset_id))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            num_resources = body['result'].get('num_resources', 0)
            if body['success'] and num_resources > 0:
                print(' Number Of Resources: %d' % num_resources)
                for resource in body['result']['resources']:
                    url = resource['url']
                    filename = '%s.%s' % (resource['id'], resource['format'].lower())
                    print(' download from %s to %s' % (url, filename))
                    self.download(url, filename)
                    # with http.request('GET', url, preload_content=False) as res, open(filename, 'wb') as out_file:
                    #     shutil.copyfileobj(res, out_file)

    def resource_show_cli(self, resource_id=''):
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/resource_show?id=%s' % (self.server_url, resource_id))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            print(json.dumps(body, sort_keys=True, indent=4))
        else:
            print('status=', r.status)

    def resource_download_cli(self, resource_id=''):
        http = urllib3.PoolManager()
        r = http.request('GET', '%s/api/3/action/resource_show?id=%s' % (self.server_url, resource_id))
        if r.status == 200:
            body = json.loads(r.data.decode('utf-8'))
            url = body['result']['url']
            filename = '%s.%s' % (body['result']['id'], body['result']['format'].lower())
            print('download: %s' % url)
            print('filename: %s' % filename)
            with http.request('GET', url, preload_content=False) as res, open(filename, 'wb') as out_file:
                shutil.copyfileobj(res, out_file)
            print('OK')
        else:
            print('Fail with ', r.status)

    def download(self, url, filename):
        with open(filename, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 10)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')

