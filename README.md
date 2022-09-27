# web3.0_etl_and_backend

## Environment set up

In terminal, type:

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## crawl event

Start the ETL process by running run_etl.py

-   Example

```
python3 run_etl.py token_events_collector -ca 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c -s 20045095 -e 20045096 -b 1000 -B 5000 -w 5 -p https://bsc-dataseed1.binance.org/ --abi bep_20
```
