import httpx
import asyncio
import json
import ssl
import argparse


async def check_ssl_cert(url: str):
    """
    This function asynchronously checks the SSL certificate of a given URL using the httpx library.
    It attempts to establish a connection to the URL and verifies the SSL certificate. If the connection is successful and the SSL certificate is valid,
    it returns a dictionary indicating the URL is valid. If there is an HTTP status error, a connection error, or an SSL certificate verification error,
    it catches these exceptions and returns a dictionary indicating the type of error encountered.

    Parameters:
    - url (str): The URL to check the SSL certificate for.

    Returns:
    - dict: A dictionary containing the URL and the status of the SSL certificate check. The status will be either "valid" if the SSL certificate is valid,
              or an error message indicating the type of error encountered.

    Raises:
    - httpx.HTTPStatusError: Raised if there is an HTTP status error during the request.
    - httpx.ConnectError: Raised if there is a connection error during the request.
    - ssl.SSLCertVerificationError: Raised if there is an SSL certificate verification error.
    """
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
    """
    This asynchronous function, `main`, takes a list of URLs as input and concurrently checks the SSL certificates of each URL using the `check_ssl_cert` function.
    It utilizes `asyncio.gather` to run multiple instances of `check_ssl_cert` in parallel, significantly speeding up the process when dealing with multiple URLs.
    The function returns a list of dictionaries, where each dictionary contains the URL and the status of its SSL certificate check.

    Parameters:
    - urls (list): A list of URLs to check the SSL certificates for.

    Returns:
    - list: A list of dictionaries, where each dictionary contains the URL and the status of its SSL certificate check. The status will be either "valid" if the SSL certificate is valid,
              or an error message indicating the type of error encountered.

    Raises:
    - Exception: Any exception raised by the `check_ssl_cert` function will propagate through this function.
    """
    return await asyncio.gather(*(check_ssl_cert(url) for url in urls))


def parse_arguments():
    """
    This function, `parse_arguments`, is designed to parse command-line arguments for a script that checks SSL certificates of given URL(s).
    It uses the argparse module to define and handle command-line arguments. The script supports two mutually exclusive modes:
    - Checking the SSL certificate of a single URL specified via the `-u` or `--url` argument.
    - Checking the SSL certificates of multiple URLs listed in a file specified via the `-f` or `--input-file` argument.

    The function first creates an ArgumentParser object with a description. It then adds a mutually exclusive group to the parser, which requires exactly one of the two arguments to be provided. If the `-u` or `--url` argument is provided, it is treated as a single URL to check. If the `-f` or `--input-file` argument is provided, the function attempts to read the file, strip whitespace from each line, and treat each line as a separate URL to check. If the file does not exist, a FileNotFoundError is caught, an error message is printed, and the script exits.

    Parameters:
    - None

    Returns:
    - list: A list of URLs to check the SSL certificates for. This list contains either a single URL or multiple URLs read from a file.

    Raises:
    - FileNotFoundError: Raised if the input file specified by the `-f` or `--input-file` argument does not exist.
    """
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
