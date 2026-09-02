# Simple Packet Analysis Lab

No Docker, no networking setup, no root/admin permissions needed.
Just two Python scripts and Wireshark (optional but recommended).

## What you're actually doing

1. A script **builds** a small file of realistic network traffic (a DNS
   lookup, a webpage request, some pings) -- all constructed in memory,
   nothing sent over a real network.
2. A second script **reads** that file and explains what's in it.
3. You can also open the file in **Wireshark** to see it visually.

That's the whole loop real analysts use: capture (or here, generate)
traffic -> inspect it -> understand what happened.

## Quick concepts (30 seconds)

- **Packet** -- a single chunk of data sent over a network. Think of it
  like an envelope: it has a "from" address, a "to" address, and some
  contents inside.
- **Protocol** -- the "language" a packet is written in. Common ones:
  - **DNS** -- "what's the IP address for this website name?"
  - **TCP** -- the reliable, ordered connection type most web traffic uses.
    Starts with a 3-step handshake: **SYN**, **SYN-ACK**, **ACK**.
  - **HTTP** -- the actual "give me this webpage" request, riding inside TCP.
  - **ICMP** -- what the `ping` command uses to check if something's reachable.
- **pcap file** -- a saved recording of packets. Short for "packet capture."
  This is the file format Wireshark opens.

## Setup

```bash
pip install scapy
```

That's the only dependency.

## Run it

```bash
python3 generate_traffic.py
```

This creates `sample_traffic.pcap` -- 13 packets simulating: a DNS
lookup, a TCP handshake, an HTTP request/response, and 3 pings.

```bash
python3 analyze_traffic.py sample_traffic.pcap
```

This prints:
1. Every packet, one line each, in plain English
2. A count of how many packets used each protocol
3. Which pairs of computers were "talking" to each other

## Look at it in Wireshark (optional but worth doing)

Open `sample_traffic.pcap` in Wireshark. Click through the packets one
at a time and compare what you see to the plain-English output from
`analyze_traffic.py` -- you'll notice it's showing you the exact same
information, just with a different presentation. Try typing `dns`,
`tcp`, or `icmp` into Wireshark's filter bar to isolate one protocol.

## Try it yourself

1. Open `generate_traffic.py` and change `example.com` to a different
   website name, or add a few more ICMP pings. Re-run both scripts and
   see how the output changes.
2. In `analyze_traffic.py`, the `describe_packet()` function decides
   how to print each packet type. Try adding a new case -- e.g. print
   the actual TCP sequence number next to each packet.
3. Pick any one packet from the walkthrough output and find that exact
   packet in Wireshark. Confirm the source IP, destination IP, and
   protocol match.

## When you're ready for more

The full lab (`packet-analysis-lab.zip` from earlier) builds on these
exact same ideas -- Scapy for building/reading packets, protocol
identification, "who talked to whom" analysis -- but adds a real
multi-hop network (via Docker) so you're capturing genuine traffic
instead of synthetic packets, and a traceroute exercise that maps an
actual path hop by hop. Nothing here becomes obsolete; it's the same
foundation, just with real networking underneath instead of a
generated file.
