import os

from dotenv import load_dotenv

load_dotenv()


class MongoDBConfig:
    USERNAME = os.environ.get("MONGODB_USERNAME", "username")
    PASSWORD = os.environ.get("MONGODB_PASSWORD", "password")
    HOST = os.environ.get("MONGODB_HOST", "0.0.0.0")
    PORT = os.environ.get("MONGODB_PORT", "27017")
    LOCAL_CONNECTION_URL = f"mongodb://{HOST}:{PORT}"
    CONNECTION_URL = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"

    DATABASE = os.environ.get("DATABASE", "bsc_data")
    COLLECTION = os.environ.get("COLLECTION", "bep_20_events")


class SanicConfig:
    RUN_SETTING = {
        "host": os.environ.get("SERVER_HOST", "localhost"),
        "port": int(os.environ.get("SERVER_PORT", 8080)),
        "debug": True,
        "access_log": False,
        "auto_reload": True,
        "workers": 4,
    }


class Provider:
    PUBLIC_RPC_NODE: str = os.environ.get(
        "PUBLIC_RPC_NODE",
        "https://bsc-dataseed1.binance.org/",
    )
