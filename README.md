# HoneyTrap
A minimal pure-Python TCP honeypot that listens on a port, greets connections with a fake service banner, and logs who knocked.

## What it does
- Listens on a TCP port and accepts incoming connections using raw server-side sockets, with no third-party libraries.
- Greets every client the instant it connects with a fake SSH banner, so a scanner logs the port as a live service and is tempted to poke further.
- Records the source IP, source port, timestamp, and first chunk of data for every connection to a log file, which is the fingerprint of who knocked and what they tried to say.
- Handles each connection in its own thread, so one slow or silent client can't block the server from accepting everyone else.
- Survives hostile input: a client that sends non-UTF-8 bytes or drops the connection mid-exchange is logged and shrugged off instead of crashing the server.
- Rebinds its port immediately on restart via `SO_REUSEADDR`, so a killed server can come straight back up without waiting out the kernel's TIME_WAIT window.
- Shuts down cleanly on Ctrl+C, closing its listening socket on the way out.

## How it works
- One listening socket is bound to a host and port and loops on `accept()`, blocking until a client connects.
- Each accepted connection is a brand-new socket dedicated to that one client; the listening socket only ever hears the knock, while the per-client socket sends the banner, reads the data, and logs the hit.
- Every new connection is handed to a fresh thread so the main loop can return to `accept()` immediately.

## Requirements
Pure Python standard library — nothing to install.

## How to run
    python honeytrap.py

Starts the server listening on `127.0.0.1:8080` (hardcoded for now) and writes hits to `honeytrap.log` in the working directory. In another terminal, connect with `nc 127.0.0.1 8080`, type something and hit enter, and the server sends its banner, prints the client's address, and appends the connection to the log.