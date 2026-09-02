# HoneyTrap
A minimal Python TCP server that listens on a port and reports who connects — the seed of a honeypot.

## What it does
- Listens on a TCP port and accepts incoming connections using raw server-side sockets, no third-party libraries.
- Reports the source IP and port of every client that connects, which is the fingerprint of who knocked on the port.
- Reads and prints the first chunk of data each client sends after connecting, so you can see what a connection tried to say.
- Wraps the socket setup in a small `TCPServer` class (`bind` / `listen` / `accept`), keeping the connection handling reusable instead of loose script code.

## How it works
- The server binds one socket to a host and port and loops on `accept()`, blocking until a client connects.
- Each accepted connection is a brand-new socket dedicated to that one client; the listening socket only ever hears the knock, while the per-client socket does the talking.

## Requirements
Python standard library — nothing to install.

## How to run
    python honeytrap.py

Starts the server listening on `127.0.0.1:8080` (hardcoded for now). In another terminal, connect with `nc 127.0.0.1 8080`, type something and hit enter, and the server prints the client's address and whatever it sent.