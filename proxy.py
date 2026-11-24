"""Entrypoint: loopback-only byte-range cache proxy for Antarctica REMA v2.0.

Run: python3 proxy.py
Env overrides: REMA_CACHE_UPSTREAM, REMA_CACHE_PORT, REMA_CACHE_DB
"""
import os

from range_cache_proxy import run_server
from source import SOURCE

if __name__ == "__main__":
    port = int(os.environ.get("REMA_CACHE_PORT", "8103"))
    db = os.environ.get("REMA_CACHE_DB", "rema-cache.sqlite3")
    server, proxy = run_server(SOURCE, db, port)
    print(f"rema cache proxy on http://127.0.0.1:{port} -> upstream {proxy.upstream_base}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        proxy.close()
