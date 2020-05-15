from prometheus_client import start_http_server, Gauge
from bitcoinrpc.authproxy import AuthServiceProxy
import getopt, sys, configparser, logging, time, requests
import cfscrape
import http.client
import json

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:v", ["config="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        sys.exit(2)
    configfile = './config.ini'
    for o, a in opts:
        if o in ("-c", "--config"):
            configfile = a

    config = configparser.ConfigParser()

    config.read_file(open(configfile))
    LTC_SERVER = config['ltc']['server_address']
    LTC_USER = config['ltc']['rpc_user']
    LTC_PASSWORD = config['ltc']['rpc_password']
    LTC_PORT = config['ltc']['rpc_port']
    EXPORTER_PORT = int(config['prometheus']['exporter_port'])
    ETALON_LTC_SERVER = config['ltc']['etalon_server_address']
    ETALON_LTC_URI = config['ltc']['etalon_server_uri']
    ETALON_LTC_KEY = config['ltc']['etalon_server_key']
    SCRAPE_INTERVAL = int(config['prometheus']['scrape_interval'])

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                level=logging.INFO)

    LTC_LAST_ETALON_BLOCK = Gauge('ltc_last_etalon_block', 'Last block in etalon blockchain')
    LTC_LAST_BLOCK = Gauge('ltc_last_block', 'Last block in our blockchain')

    start_http_server(EXPORTER_PORT)

    while True:
        try:
            rpc_connection = AuthServiceProxy("http://{}:{}@{}:{}".format(LTC_USER, LTC_PASSWORD, LTC_SERVER, LTC_PORT))
            blockchain_info = rpc_connection.getblockchaininfo()
            lastOurBlock = blockchain_info['blocks']
        except Exception as err:
            logging.error("Can't get latest blocks from our blockchain!")
            logging.error(err)
            lastOurBlock = 0
        try:
            conn = http.client.HTTPSConnection(ETALON_LTC_SERVER)
            headers = {
              'Content-Type': "application/json",
              'X-API-Key': ETALON_LTC_KEY
            }
            conn.request("GET", ETALON_LTC_URI, headers=headers)
            r = conn.getresponse()
            data = json.loads(r.read().decode("utf-8"))
            lastEtalonBlock = data['payload']['height']
        except Exception as err:
            logging.error("Can't get latest blocks from etalon blockchain!")
            logging.error(err)
            lastEtalonBlock = 0
        LTC_LAST_ETALON_BLOCK.set(lastEtalonBlock)
        LTC_LAST_BLOCK.set(lastOurBlock)
        print('LTC_LAST_ETALON_BLOCK: ' + str(lastEtalonBlock))
        print('LTC_LAST_BLOCK: ' + str(lastOurBlock))
        time.sleep(SCRAPE_INTERVAL)
    
if __name__ == '__main__':
    main()
