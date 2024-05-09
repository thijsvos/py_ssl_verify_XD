import httpx
import asyncio
import json
import ssl
import argparse


async def check_ssl_cert(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return {"url": url, "status": "valid"}

    except httpx.HTTPStatusError as e:
        return {"url": url, "status": f"error: {str(e)}"}
    except httpx.ConnectError as e:
        return {"url": url, "status": f"error: {str(e)}"}
    except ssl.SSLCertVerificationError as e:
        return {"url": url, "status": f"error: {str(e)}"}


async def main(urls):
    return await asyncio.gather(*(check_ssl_cert(url) for url in urls))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Check SSL certificates of given URL(s).')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--input-file', type=str, help='Path to the input file containing URLs')
    group.add_argument('-u', '--url', type=str, help='Single URL to check')
    args = parser.parse_args()
    if args.url:
        parsed_urls = [args.url]
    elif args.input_file:
        try:
            with open(args.input_file, 'r') as file:
                parsed_urls = [line.strip() for line in file.readlines()]
        except FileNotFoundError as e:
            print(f"{e}")
            quit()
    return parsed_urls


if __name__ == "__main__":
    urls = parse_arguments()
    results = asyncio.run(main(urls))
    json_results = json.dumps(results, indent=4, ensure_ascii=False)
    print(json_results)
