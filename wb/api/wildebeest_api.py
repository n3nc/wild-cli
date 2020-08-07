import urllib3
import urllib
import json
import shutil
import os
import requests
import sys

class WildebeestApi(object):
    __version__ = '1.0.4'
    server_url = ''
    api_key = None

    def __init__(self):
        self.server_url = os.environ.get('WB_SERVER_URL')
        self.api_key = os.environ.get('WB_API_KEY', None)

    def organizations_list_cli(self):
        result = self.GetResult('/api/3/action/organization_list')
        if result is not None:
            print(' %-20s %-30s %10s' % ('NAME', 'DISPLAY NAME', 'DATASETS'))
            for i in result:
                result = self.GetResult('/api/3/action/organization_show?id=%s' % i)
                if result is not None:
                    print(' %-20s %-30s %10d' % (i, result['display_name'], result['package_count']))

    def organizations_show_cli(self, organization_id):
        print(json.dumps(self.GetResult('/api/3/action/organization_show?id=%s' % organization_id), sort_keys=True, indent=4))

    def organizations_datasets_cli(self, organization_id, page):
        result = self.GetResult('/api/3/action/package_search?&include_private=True&q=organization:%s&rows=20&start=%d' %
                            (organization_id, (int(page)-1) * 20))
        if result is not None:
            print(' Found: %d' % result.get('count'))
            print('%38s %-75s %9s' % ('ID', 'TITLE', 'RESOURCES'))
            if 'results' in result.keys():
                for dataset in result['results']:
                    print(' %36s %-80s %4d' % (dataset['id'], dataset['title'][:80], dataset['num_resources']))


    def datasets_list_cli(self, page=1):
        result = self.GetResult('/api/3/action/package_search?&include_private=True&rows=20&start=%d' % ((int(page)-1) * 20))
        if result is None:
            return
        print(' Found: %d' % result.get('count'))
        print('%38s %-75s %9s' % ('ID', 'TITLE', 'RESOURCES'))
        for result in result['results']:
            print(' %36s %-80s %4d' % (result['id'], result['title'][:80], result['num_resources']))

    def datasets_show_cli(self, dataset_id):
        print(json.dumps(self.GetResult('/api/3/action/package_show?id=%s' % dataset_id), sort_keys=True, indent=4))

    def datasets_search_cli(self, query='', page=1):
        result = self.GetResult('/api/3/action/package_search?&include_private=True&{}&rows=20&start={}'.format(urllib.parse.urlencode({'q': query}), ((int(page)-1) * 20)))
        if result is None:
            return
        print(' Found: %d' % result.get('count'))
        print(' %36s %-75s %9s' % ('ID', 'TITLE', 'RESOURCES'))
        for result in result['results']:
            print(' %36s %-80s %4d' % (result['id'], result['title'][:80], result['num_resources']))

    def datasets_resources_cli(self, dataset=''):
        result = self.GetResult('/api/3/action/package_show?id=%s' % dataset)
        if result is not None and result['num_resources'] > 0:
            print(' Found: %d' % result['num_resources'])
            print('%38s %100s %10s %5s' % ('ID', 'NAME', 'FORMAT', 'DS'))
            for i in result['resources']:
                print(' %36s %100s %10s %5s' % (i['id'], i['name'], i['format'][:100], i['datastore_active']))

    def datasets_download_cli(self, dataset_id):
        result = self.GetResult('/api/3/action/package_show?id=%s' % dataset_id)
        if result is not None:
            num_resources = result.get('num_resources', 0)
            print(' Number Of Resources: %d' % num_resources)
            if num_resources > 0:
                for resource in result['resources']:
                    url = resource['url']
                    filename = '%s.%s' % (resource['id'], resource['format'].lower())
                    print(' download from %s to %s' % (url, filename))
                    self.download(url, filename)
        else:
            print('Fail with ', r.status)

    def resource_show_cli(self, resource_id=''):
        print(json.dumps(self.GetResult('/api/3/action/resource_show?id=%s' % resource_id), sort_keys=True, indent=4))

    def resource_download_cli(self, resource_id=''):
        result = self.GetResult('/api/3/action/resource_show?id=%s' % resource_id)
        if result is not None:
            url = result['url']
            filename = '%s.%s' % (result['id'], result['format'].lower())
            print(' download from %s to %s' % (url, filename))
            self.download(url, filename)
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
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')

    def Get(self, url):
        http = urllib3.PoolManager()
        headers = None
        if self.api_key is not None:
            headers = {'Authorization': self.api_key}
        r = http.request('GET', '%s%s' % (self.server_url, url), None, headers)
        if r.status == 200:
            return json.loads(r.data.decode('utf-8'))
        else:
            print('Fail with ', r.status)
        return None

    def GetResult(self, url):
        body = self.Get(url)
        if body is not None and body['success']:
            return body['result']
        return None

