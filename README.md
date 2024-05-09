# py_ssl_verify_XD

## Install
```
pip install httpx
```

## Usage

```
usage: main.py [-h] (-f INPUT_FILE | -u URL)

Check SSL certificates of given URL(s).

options:
  -h, --help            show this help message and exit
  -f INPUT_FILE, --input-file INPUT_FILE
                        Path to the input file containing URLs
  -u URL, --url URL     Single URL to check
```

## Example
```
python main.py -u https://example.com 
[
    {
        "url": "https://example.com",
        "status": "valid"
    }
]
```

```
python main.py -f xd.txt 
[
    {
        "url": "https://expired.badssl.com/",
        "status": "error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1000)"
    },
    {
        "url": "https://wrong.host.badssl.com/",
        "status": "error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'wrong.host.badssl.com'. (_ssl.c:1000)"
    },
    {
        "url": "https://self-signed.badssl.com/",
        "status": "error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1000)"
    },
    {
        "url": "https://untrusted-root.badssl.com/",
        "status": "error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)"
    },
    {
        "url": "https://revoked.badssl.com/",
        "status": "error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1000)"
    },
    {
        "url": "https://pinning-test.badssl.com/",
        "status": "valid"
    },
    {
        "url": "https://badssl.com/",
        "status": "valid"
    }
]
```
