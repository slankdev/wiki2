
# Tshark / tshark

```
tshark -i eth0
tshark -r in.pcap -c10                                ##10packet output
tshark -r in.pcap -f "tcp port 80"                    ##apply capture filter
tsahrk -r in.pcap -R "tcp.port == 80"                 ##apply display filter
tshark -r in.pcap -d tcp.port==8080,http              ##apply TCP8080 is http
tshark -r in.pcap -V                                  ##Print as tree-format
tshark -r in.pcap -x                                  ##Print packet hexdump

tshark -r in.pcap -T json                             ##Specify output format (json)
tshark -r in.pcap -T fields ${ELEMENT_OPTIONS}        ##Specify output format (specified-fields, see following cheatsheet)
tshark -r in.pcap -T fields -e frame.protocols        ##Specify output format (specified-fields, prints only protocol)
tshark -r in.pcap -T ${TEXT_TYPE}                     ##Specify output format
   TEXT_TYPE
        "pdml"    Packet Details Markup Language, an XML-based format
        "ps"      PostScript for a human-readable one-line summary
        "psml"    Packet Summary Markup Language, an XML-based format
        "json"    Packet Summary, an JSON-based format
        "jsonraw" Packet Details, a JSON-based format
        "ek"      Packet Details, an EK JSON-based format
        "text"    Text of a human-readable one-line summary
        "tabs"    Similar to the text report.
```

## Option e's cheatsheet (``-e <field-name>``)

| name |  example-output  |
| :---- | :---------------- |
| ``frame.len``    | ``98`` |
| ``frame.number`` | ``1``  |
| ``frame.protocols`` | ``http``  |
| ``_ws.col.Info`` | ``Echo (ping) request  id=0x14f7, seq=1/256, ttl=64`` |

## examples

```
# tshark -D
1. enp0s3
2. enp0s8
3. enp0s9
4. any
5. lo (Loopback)
7. nflog
8. nfqueue
9. ciscodump (Cisco remote capture)
10. randpkt (Random packet generator)
11. sshdump (SSH remote capture)
12. udpdump (UDP Listener remote capture)
```
```
# tshark -r in.pcap -T fields -e frame.number -e frame.len -e _ws.col.Info
1       98      Echo (ping) request  id=0x14f7, seq=1/256, ttl=64
2       98      Echo (ping) reply    id=0x14f7, seq=1/256, ttl=64 (request in 1)
3       98      Echo (ping) request  id=0x14f7, seq=2/512, ttl=64
4       98      Echo (ping) reply    id=0x14f7, seq=2/512, ttl=64 (request in 3)
5       98      Echo (ping) request  id=0x14f7, seq=3/768, ttl=64
6       98      Echo (ping) reply    id=0x14f7, seq=3/768, ttl=64 (request in 5)<Paste>
```
