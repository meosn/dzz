import os
import json
import time
import urllib.parse
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise SystemExit("Нет OPENWEATHER_API_KEY в переменных окружения")
API_KEY = API_KEY.strip()

MAX_WORKERS = 8
CHUNK_SIZE = 10

GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

lock = threading.Lock()
q = Queue()

def chunked(arr, n):
    for i in range(0, len(arr), n):
        yield arr[i:i+n]

def parse_cc(city_line):
    parts = [p.strip() for p in city_line.split(",") if p.strip()]
    if len(parts) >= 2:
        return parts[-1]
    return None

def get_json_with_retry(url, params, timeout=10):
    delays = [0.0, 0.5, 1.0]
    last_err = None
    for d in delays:
        if d:
            time.sleep(d)
        try:
            r = requests.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r.json(), None
            if r.status_code == 429 or 500 <= r.status_code <= 599:
                last_err = f"HTTP {r.status_code}"
                continue
            return None, f"HTTP {r.status_code}: {r.text[:200]}"
        except Exception as e:
            last_err = str(e)
    return None, last_err

def resolve_city(city_line):
    params = {"q": city_line, "limit": 5, "appid": API_KEY}
    data, err = get_json_with_retry(GEO_URL, params)
    if err:
        return None, err
    if not data:
        return None, "geocoding: 0 results"

    cc = parse_cc(city_line)
    chosen = None
    if cc and len(data) > 1:
        for c in data:
            if c.get("country") == cc:
                chosen = c
                break
    if not chosen:
        chosen = data[0]

    ambiguous = (len(data) > 1 and not (cc and chosen.get("country") == cc))
    resolved = {
        "name": chosen.get("name"),
        "lat": chosen.get("lat"),
        "lon": chosen.get("lon"),
        "country": chosen.get("country"),
        "state": chosen.get("state"),
        "candidates": len(data),
    }
    return (resolved, ambiguous), None

def get_weather(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }
    data, err = get_json_with_retry(WEATHER_URL, params)
    if err:
        return None, err
    w = (data.get("weather") or [{}])[0]
    main = data.get("main") or {}
    wind = data.get("wind") or {}
    return {
        "temp": main.get("temp"),
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "wind": wind.get("speed"),
        "description": w.get("description"),
    }, None

def worker(cities, out_f, err_f):
    for city in cities:
        city = city.strip()
        if not city:
            q.put(("progress", None))
            continue

        resolved_pack, err = resolve_city(city)
        if err:
            with lock:
                err_f.write(f"{city}\t{err}\n")
                err_f.flush()
            q.put(("err", city))
            q.put(("progress", None))
            continue

        resolved, ambiguous = resolved_pack
        weather, err = get_weather(resolved["lat"], resolved["lon"])
        if err:
            with lock:
                err_f.write(f"{city}\t{err}\n")
                err_f.flush()
            q.put(("err", city))
            q.put(("progress", None))
            continue

        obj = {
            "input": city,
            "resolved": resolved,
            "weather": weather,
            "ts": int(time.time()),
            "ambiguous": bool(ambiguous),
        }

        with lock:
            out_f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            out_f.flush()

        q.put(("ok", city))
        q.put(("progress", None))

with open("cities.txt", "r", encoding="utf-8") as f:
    cities = [line.strip() for line in f if line.strip()]

total = len(cities)
done = ok = err = 0
last = "-"

out_f = open("weather_results.jsonl", "w", encoding="utf-8")
err_f = open("errors.log", "w", encoding="utf-8")

chunks = list(chunked(cities, CHUNK_SIZE))

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    for ch in chunks:
        ex.submit(worker, ch, out_f, err_f)

    while done < total:
        t, city = q.get()
        if t == "ok":
            ok += 1
            last = city
        elif t == "err":
            err += 1
        elif t == "progress":
            done += 1

        p = int((done / total) * 100) if total else 100
        bar_len = 20
        filled = int(bar_len * p / 100)
        bar = "[" + ("#" * filled) + ("-" * (bar_len - filled)) + "]"
        print(f"\r{bar} {p}% | done {done}/{total} | ok {ok} | err {err} | last: {last}", end="")

print()
out_f.close()
err_f.close()