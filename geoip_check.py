#!/usr/bin/python3

import sys
import aiohttp
import asyncio


SOURCES = [
    {'url': 'https://ipapi.co/{}/json/', 'key': 'country_code'},
    {'url': 'https://reallyfreegeoip.org/json/{}', 'key': 'country_code'},
    {'url': 'https://json.geoiplookup.io/{}', 'key': 'country_code'},
    {'url': 'https://api.iplocation.net/?ip={}', 'key': 'country_code2'},
    {'url': 'https://api.geoiplookup.net/?query={}&json=true', 'key': 'countrycode'},
    {'url': 'http://ip-api.com/json/{}', 'key': 'countryCode'},
    {'url': 'https://ipwhois.app/json/{}', 'key': 'country_code'},
]


def print_stat(results):
    d = {}
    for code in results:
        if code in d:
            d[code] += 1
        else:
            d[code] = 1

    for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True):
        print(f' {k}: {100 * v / len(results):.2f}% ({v} of {len(results)})')


async def get_country(session, url, key):
    async with session.get(url) as resp:
        answer = await resp.json()
        return answer.get(key, 'XX')


async def main(ip):
    async with aiohttp.ClientSession() as session:

        tasks = []
        for item in SOURCES:
            tasks.append(
                asyncio.ensure_future(
                    get_country(session, item['url'].format(ip), item['key'])
                )
            )

        results = await asyncio.gather(*tasks)

        print_stat(results)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = '8.8.8.8'  # 1.2.3.4'
    print(f'Checking IP {ip} among {len(SOURCES)} sources...')

    asyncio.run(main(ip))
