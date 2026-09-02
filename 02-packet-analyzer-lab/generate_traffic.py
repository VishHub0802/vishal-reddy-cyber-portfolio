#!/usr/bin/env python3
"""
generate_traffic.py

Builds a small, realistic-looking pcap file WITHOUT sending anything over
a real network. We're just constructing packet objects in memory (the way
you'd build a LEGO model without needing a LEGO factory) and saving them
to a file. This means no root/admin permissions are needed and nothing
ever leaves your machine.

The file will contain:
  - A DNS query + response  (someone looking up a website's IP address)
  - A TCP three-way handshake (SYN, SYN-ACK, ACK - how connections start)
  - An HTTP GET request + response (a simple webpage fetch)
  - A few ICMP pings (like the 'ping' command)

Run:
    python3 generate_traffic.py
Produces:
    sample_traffic.pcap
"""
from scapy.all import (
    IP, TCP, UDP, ICMP, DNS, DNSQR, DNSRR, Raw, wrpcap
)

packets = []

CLIENT = "192.168.1.50"
SERVER = "93.184.216.34"     # a made-up "web server" address
DNS_SERVER = "8.8.8.8"

# --- 1. DNS query: client asks "what's the IP for example.com?" ---
dns_query = (
    IP(src=CLIENT, dst=DNS_SERVER)
    / UDP(sport=53211, dport=53)
    / DNS(rd=1, qd=DNSQR(qname="example.com"))
)
packets.append(dns_query)

# --- 2. DNS response: DNS server answers ---
dns_response = (
    IP(src=DNS_SERVER, dst=CLIENT)
    / UDP(sport=53, dport=53211)
    / DNS(qr=1, qd=DNSQR(qname="example.com"),
          an=DNSRR(rrname="example.com", rdata=SERVER))
)
packets.append(dns_response)

# --- 3. TCP three-way handshake: client connects to the web server ---
syn = IP(src=CLIENT, dst=SERVER) / TCP(sport=44321, dport=80, flags="S", seq=1000)
syn_ack = IP(src=SERVER, dst=CLIENT) / TCP(sport=80, dport=44321, flags="SA", seq=5000, ack=1001)
ack = IP(src=CLIENT, dst=SERVER) / TCP(sport=44321, dport=80, flags="A", seq=1001, ack=5001)
packets += [syn, syn_ack, ack]

# --- 4. HTTP GET request + response (plain text, easy to read in Wireshark) ---
http_request = (
    IP(src=CLIENT, dst=SERVER)
    / TCP(sport=44321, dport=80, flags="PA", seq=1001, ack=5001)
    / Raw(load=b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
)
http_response = (
    IP(src=SERVER, dst=CLIENT)
    / TCP(sport=80, dport=44321, flags="PA", seq=5001, ack=1050)
    / Raw(load=b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello world!\r\n")
)
packets += [http_request, http_response]

# --- 5. A handful of ICMP pings, like running `ping example.com` ---
for seq in range(1, 4):
    packets.append(IP(src=CLIENT, dst=SERVER) / ICMP(seq=seq))
    packets.append(IP(src=SERVER, dst=CLIENT) / ICMP(type=0, seq=seq))  # echo-reply

wrpcap("sample_traffic.pcap", packets)
print(f"Wrote {len(packets)} packets to sample_traffic.pcap")
print("Open this file in Wireshark, or run: python3 analyze_traffic.py sample_traffic.pcap")
