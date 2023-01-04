import requests
import argparse

parser = argparse.ArgumentParser(description='')

parser.add_argument('--url', type=str, default='127.0.0.1')
parser.add_argument('--port', type=str, default='5000')
parser.add_argument('--image', type=str, default=None)

args = parser.parse_args()

def send_data(url, args):
    files = {
        'file' : open(args.image, 'rb')
    }
    res = requests.post(url)

url = args.url + ':' + args.port
print('[DEBUG]', send_data(url, args))
