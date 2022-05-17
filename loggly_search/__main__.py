import asyncio
import json

import configargparse
import httpx
import yarl


class Loggly:

    def __init__(self, subdomain, token):
        self.client = httpx.AsyncClient()
        self.client.headers['Authorization'] = f'bearer {token}'
        self.url = yarl.URL(f'https://{subdomain}.loggly.com')

    async def search(self, query, start, end, order):
        url = str((self.url / 'apiv2' / 'events' / 'iterate').with_query({
                'q': query,
                'from': start,
                'until': end,
                'order': order,
                'size': 1000,  # API max
            }))

        while url:
            # disable timeout as some searches take longer than the default
            response = await self.client.get(url, timeout=None)
            body = response.json()
            url = body.get('next')
            for event in body.get('events', []):
                yield event


async def _async_main(args):
    client = Loggly(subdomain=args.subdomain, token=args.token)

    future = client.search(
        query=args.query,
        start=args.start,
        end=args.end,
        order=args.order)

    num_events = 0
    async for event in future:
        print(json.dumps(event))
        num_events += 1
        if args.limit and num_events == args.limit:
            break


def main():
    parser = configargparse.ArgumentParser()
    parser.add_argument('--token', env_var='LOGGLY_TOKEN')
    parser.add_argument('--subdomain', env_var='LOGGLY_SUBDOMAIN')

    parser.add_argument('--from', default='-24h', dest='start')
    parser.add_argument('--to', default='now', dest='end')
    parser.add_argument('--order', choices=('asc', 'desc'), default='asc')
    parser.add_argument('--limit', type=int, dest='limit')
    parser.add_argument('query')

    args = parser.parse_args()

    asyncio.run(_async_main(args))


if __name__ == '__main__':
    main()
