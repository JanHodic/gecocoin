# CryptoStack


## Spuštění
1) `docker compose up --build`
2) Frontend: http://localhost:8080
3) API swagger: http://localhost:8000/docs


## Příklady
```bash
# Vytvořit coin
curl -X POST http://localhost:8000/coins/ -H 'Content-Type: application/json' -d '{"symbol":"btc"}'
# Seznam
curl http://localhost:8000/coins/
# Refresh jednoho
curl -X POST http://localhost:8000/coins/1/refresh
# Refresh všech
curl -X POST http://localhost:8000/coins/refresh-all

---
## ✨ Poznámky
- Redis je využit pro **cache** odpovědí z CoinGecko (TTL 2–5 min) → šetří limity.
- CORS je nastaven pro `http://localhost:8080` (pokud proxy nepoužiješ). V téhle šabloně frontend volá **/api** přes Nginx, takže CORS většinou netřeba.
- Pro produkci přidej Alembic migrace, autentizaci, testy (Pytest), rate-limiting a lepší chybové kódy.