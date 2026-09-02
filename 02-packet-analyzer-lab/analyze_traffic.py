#!/usr/bin/env python3
"""
analyze_traffic.py

Reads a pcap file and prints a plain-English breakdown of what's in it:
protocol counts, who's talking to whom, and a plain summary of each
packet in order. This is the "manual Wireshark" -- the same information
Wireshark shows you graphically, printed out step by step so you can see
exactly how it's derived.

Run:
    python3 analyze_traffic.py sample_traffic.pcap
"""
import argparse
from collections import Counter

from scapy.all import rdpcap, IP, TCP, UDP, ICMP, DNS


def describe_packet(pkt, index):
    """Return a one-line, human-readable description of a packet."""
    if not pkt.haslayer(IP):
        return f"#{index}: (non-IP packet, skipping)"

    src, dst = pkt[IP].src, pkt[IP].dst

    if pkt.haslayer(DNS):
        dns = pkt[DNS]
        if dns.qr == 0:
            name = dns.qd.qname.decode() if dns.qd else "?"
            return f"#{index}: DNS QUERY   {src} -> {dst}   \"who has {name}?\""
        else:
            answer = dns.an.rdata if dns.an else "?"
            return f"#{index}: DNS REPLY   {src} -> {dst}   \"it's {answer}\""

    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        flags = tcp.sprintf("%TCP.flags%")
        extra = ""
        if pkt.haslayer("Raw"):
            payload = bytes(pkt["Raw"].load)
            first_line = payload.split(b"\r\n")[0].decode(errors="replace")
            extra = f'   payload: "{first_line}"'
        return f"#{index}: TCP [{flags:<3}] {src}:{tcp.sport} -> {dst}:{tcp.dport}{extra}"

    if pkt.haslayer(ICMP):
        icmp = pkt[ICMP]
        kind = "REQUEST" if icmp.type == 8 else "REPLY" if icmp.type == 0 else f"type={icmp.type}"
        return f"#{index}: ICMP {kind:<8} {src} -> {dst}   seq={icmp.seq}"

    if pkt.haslayer(UDP):
        return f"#{index}: UDP {src}:{pkt[UDP].sport} -> {dst}:{pkt[UDP].dport}"

    return f"#{index}: IP {src} -> {dst}  (other)"


def main():
    ap = argparse.ArgumentParser(description="Beginner-friendly pcap analyzer")
    ap.add_argument("pcap_file")
    args = ap.parse_args()

    packets = rdpcap(args.pcap_file)
    print(f"Loaded {len(packets)} packets from {args.pcap_file}\n")

    # --- 1. Walk through every packet in order, plain English ---
    print("=" * 70)
    print("PACKET-BY-PACKET WALKTHROUGH")
    print("=" * 70)
    for i, pkt in enumerate(packets, start=1):
        print(describe_packet(pkt, i))

    # --- 2. Protocol breakdown ---
    proto_counter = Counter()
    for pkt in packets:
        if pkt.haslayer(DNS):
            proto_counter["DNS"] += 1
        elif pkt.haslayer(TCP):
            proto_counter["TCP"] += 1
        elif pkt.haslayer(ICMP):
            proto_counter["ICMP"] += 1
        elif pkt.haslayer(UDP):
            proto_counter["UDP"] += 1
        else:
            proto_counter["Other"] += 1

    print("\n" + "=" * 70)
    print("PROTOCOL BREAKDOWN")
    print("=" * 70)
    for proto, count in proto_counter.most_common():
        bar = "#" * count
        print(f"{proto:<8} {count:>3}  {bar}")

    # --- 3. Who's talking to whom ---
    conversations = Counter()
    for pkt in packets:
        if pkt.haslayer(IP):
            pair = tuple(sorted([pkt[IP].src, pkt[IP].dst]))
            conversations[pair] += 1

    print("\n" + "=" * 70)
    print("CONVERSATIONS (who talked to whom, and how many packets)")
    print("=" * 70)
    for (a, b), count in conversations.most_common():
        print(f"{a}  <->  {b}   ({count} packets)")


if __name__ == "__main__":
    main()
