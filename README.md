# web3.0_etl_and_backend

## Environment set up

In terminal, type:

```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip3 install -r requirements.txt
```

## Basic configuration

By default, it will connect to MongoDB at `localhost:27017` and create a collection named `bep_20_events` in the database named `bsc_data`. To change the connection URL, database and collection name, create and edit the `.env` file to the desired values.

## Events crawling

Collecting data of events emitted by BEP-20 smart contracts from BscScan public RPC Nodes.

Inspired by [Evgeny Medvedev](https://github.com/medvedev1088)'s [ethereum-etl](https://github.com/blockchain-etl/ethereum-etl).

---

Start the ETL process by running run_etl.py

-   Example: Get all events emitted by WBNB token from block 20045095 to block 20045096

```bash
> python3 run_etl.py token_events_collector -ca 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c -s 20045095 -e 20045096 -b 1000 -B 5000 -w 5 -p https://bsc-dataseed1.binance.org/ --abi bep_20
```

## API

A simple API written in Sanic to interact with crawled data.

---

Start the API by running run_api.py

-   Example:

```bash
> python3 run_api.py
```
