# Ansible-Litecoind

This repository contains role for instaling container with Litecoind-core blockchain and simple Prometheus exporter

## Variables

* `litecoind_home: '/opt/litecoind'` - directory for blockchain data
* `litecoind_versoin: 'latest'` - litecoin docker image tag
* `litecoind_rpcuser: 'rpcuser'` - user for RPC authorization
* `litecoind_rpcpassword: 'rpcpassword'` - password for RPC authorization
* `litecoind_rpcport: 9322` - RPC port
* `litecoin_network: 'mainnet'` - LTC network (mainnet/testnet)
* `ltc_user: 'ltc'` - restricted user for monitoring script
* `ltc_exporter_home: '/opt/ltc_exporter'` - directory for ltc exporter script
* `ltc_exporter_port: 8557` - port for ltc exporter script
* `ltc_cryptoapis_key: longapikey` - API key for <https://cryptoapis.io/?utm_source=package_info> services
* `ltc_exporter_interval: 600` - how often (in seconds) need to fetch info about blocks

## Prometheus exporter

This is very simple script, which provides following metrics:

```bash
# Some default Python metrics skipped

# HELP ltc_last_block Last block in our blockchain
# TYPE ltc_last_block gauge

# HELP ltc_last_etalon_block Last block in etalon blockchain
# TYPE ltc_last_etalon_block gauge
```

As etalon blockchain, we use Blockchain APIs from <https://cryptoapis.io/?utm_source=package_info> (the free plan is enough for that simple monitoring).
