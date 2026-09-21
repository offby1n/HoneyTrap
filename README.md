# HoneyTrap

A multi-service TCP honeypot you run from the command line — it answers with a fake service banner and logs everyone who connects.

## What it does

- Poses as a real service (SSH, HTTP, or FTP) by sending a convincing banner on connect, so a scanner or attacker thinks they've hit the real thing.
- Logs every connection with a timestamp, the source address, and whatever bytes the client sent, so you can see who's probing you and with what.
- Handles many connections at once, one thread per client, so a single slow or hung connection never blocks the next one.
- Serialises all log writes behind a lock, so simultaneous connections can't corrupt the log file.
- Survives garbage input: undecodable bytes are logged with replacement characters instead of crashing the handler.
- Shuts down cleanly on Ctrl-C, closing the listening socket.

## How it works

- One base server owns the plumbing — bind, listen, accept, threading, and logging. Each fake service is a thin subclass that overrides nothing but its banner.
- The `--service` flag picks which subclass to run; the base behaviour is identical across all three.
- Logs are written to `/var/log/honeytrap.log`, which is why the tool needs `sudo` (or a systemd unit) to run.

## Install

### One-line install (curl)

    curl -fsSL https://raw.githubusercontent.com/offby1n/HoneyTrap/main/install.sh | bash

### Manual install (clone)

    git clone https://github.com/offby1n/HoneyTrap.git
    cd HoneyTrap
    bash install.sh

The installer symlinks the script to `~/.local/bin/honeytrap` so you can run it as `honeytrap` from anywhere. Make sure `~/.local/bin` is on your `PATH`.

## Updating

    curl -fsSL https://raw.githubusercontent.com/offby1n/HoneyTrap/main/install.sh | bash

Re-running the installer pulls the latest version and re-links it. If you installed from a manual clone instead, run `git pull` inside the `HoneyTrap` folder.

## How to run

    sudo honeytrap -s ssh -p 8080 -H 0.0.0.0

Runs the SSH honeypot on port 8080, bound to all interfaces. `sudo` is required because the log lives in `/var/log`. Flags:

- `-s`, `--service` — which fake service to present: `ssh`, `http`, or `ftp` (default `ssh`).
- `-p`, `--port` — TCP port to listen on (default `8080`).
- `-H`, `--host` — address to bind; `0.0.0.0` means all interfaces (default `0.0.0.0`).

Run `honeytrap -h` for the full help. Watch the log live with `sudo tail -f /var/log/honeytrap.log`.
