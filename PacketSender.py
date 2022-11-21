import json

import psutil

from scapy.layers.inet import IP, UDP, TCP, ICMP, Ether
from scapy.all import hexdump, sendp


# SCAPY_DEFAULT_self.PacketS = {
#     "IP": IP(
#             version =int(self.Packet_DEFAULTS["IP"]["version"]),
#             ihl     =int(self.Packet_DEFAULTS["IP"]["IHL"   ]),
#             len     =int(self.Packet_DEFAULTS["IP"]["length"]),
#             id      =int(self.Packet_DEFAULTS["IP"]["ID"    ]),
#             frag    =int(self.Packet_DEFAULTS["IP"]["offset"]),
#             ttl     =int(self.Packet_DEFAULTS["IP"]["TTL"   ]),
#             proto   =int(self.Packet_DEFAULTS["IP"]["prot"  ]),
#             src     =self.Packet_DEFAULTS["IP"]["ip_src"],
#             dst     =self.Packet_DEFAULTS["IP"]["ip_dst"]
#              ),
#     "TCP": TCP(
#             sport   =int(self.Packet_DEFAULTS["TCP"]["frm_src_port"]),
#             dport   =int(self.Packet_DEFAULTS["TCP"]["frm_dst_port"]),
#             seq     =int(self.Packet_DEFAULTS["TCP"]["frm_seq"     ]),
#             ack     =int(self.Packet_DEFAULTS["TCP"]["frm_ack"     ]),
#             dataofs =int(self.Packet_DEFAULTS["TCP"]["frm_offset"  ]),
#             window  =int(self.Packet_DEFAULTS["TCP"]["frm_window"  ]),
#             urgptr  =int(self.Packet_DEFAULTS["TCP"]["frm_up"      ])
#     ),
#     "UDP": UDP(
#             sport   =int(self.Packet_DEFAULTS["UDP"]["src_port"]),
#             dport   =int(self.Packet_DEFAULTS["UDP"]["dst_port"]),
#             len     =int(self.Packet_DEFAULTS["UDP"]["length"  ]),
#     ),
#     "ICMP": ICMP(
#             type    =self.Packet_DEFAULTS["ICMP"]["type"  ]
#     )
# }


class PacketSender():
    def __init__(self):
        self.Packet = IP()
        self.Parameters = {}
        self.Interfaces = psutil.net_if_addrs()
    
    def FormPacket(self, filename : str = None, params = None):
        del self.Packet
        self.Packet = IP()
        self.Packet[IP].version = 4 #?
        if filename != None:
            with open(filename, "r") as file:
                self.Parameters = json.load(file)
            file.close()
        elif params != None:
            self.Parameters = params.copy()
        else:
            self.Parameters = {}
            return

        
        
        for i, _ in self.Parameters.items():
            for j, field in self.Parameters[i].items():
                if field == "":
                    self.Parameters[i][j] = None

        
        if self.Parameters["IP"].get("Source"): 
            self.Packet[IP].src = self.Parameters["IP"].get("Source")
        if self.Parameters["IP"].get("Destination"): 
            self.Packet[IP].dst = self.Parameters["IP"].get("Destination")

        if self.Parameters["IP"].get("Header"): 
            self.Packet[IP].ihl = int(self.Parameters["IP"].get("Header"))
        if self.Parameters["IP"].get("Identification"): 
            self.Packet[IP].id = int(self.Parameters["IP"].get("Identification"))
        if self.Parameters["IP"].get("CheckSumIP"):
             self.Packet[IP].chksum = int(self.Parameters["IP"].get("CheckSumIP"))
        if self.Parameters["IP"].get("TotalLength"):
             self.Packet[IP].len = int(self.Parameters["IP"].get("TotalLength"))
        if self.Parameters["IP"].get("TTL"):
             self.Packet[IP].ttl = int(self.Parameters["IP"].get("TTL"))

        TOS = 0
        if self.Parameters["IP"].get("Priority"):
            TOS += (int(self.Parameters["IP"].get("Priority")) % 0b1111) << 5
        if self.Parameters["IP"].get('Service'):
            if "Delay" in self.Parameters["IP"].get('Service'):
                TOS += 0b10000
            if "Throughput" in self.Parameters["IP"].get('Service'):
                TOS += 0b01000
            if "Reliability" in self.Parameters["IP"].get('Service'):
                TOS += 0b00100
        self.Packet[IP].tos = TOS

        flags = 0
        if self.Parameters["IP"].get("Offset"):
             self.Packet[IP].frag = int(self.Parameters["IP"].get("Offset"))

        if self.Parameters["IP"].get('Fragmentation'):
            if "Reserved" in self.Parameters["IP"].get("Fragmentation"):
                flags += 0b100
            if "NoFragment" in self.Parameters["IP"].get("Fragmentation"):
                flags += 0b010
            if "MoreFragment" in self.Parameters["IP"].get("Fragmentation"):
                flags += 0b001
        self.Packet[IP].flags = flags


        payload = ""
        if self.Parameters["IP"]['Protocol'] == "TCP":
            self.Packet[IP].proto = 6
            self.Packet = self.Packet/TCP()

            if self.Parameters["TCP"].get("Source"):
                self.Packet[TCP].sport = int(self.Parameters["TCP"]["Source"])
            if self.Parameters["TCP"].get("Destination"):
                self.Packet[TCP].dport = int(self.Parameters["TCP"]["Destination"])
            if self.Parameters["TCP"].get("TCPOffset"):
                self.Packet[TCP].dataofs = int(self.Parameters["TCP"]["TCPOffset"])
            if self.Parameters["TCP"].get("Window"):
                self.Packet[TCP].window = int(self.Parameters["TCP"]["Window"])
            if self.Parameters["TCP"].get("Sequence"):
                self.Packet[TCP].seq = int(self.Parameters["TCP"]["Sequence"])
            if self.Parameters["TCP"].get("Acknolegement"):
                self.Packet[TCP].ack = int(self.Parameters["TCP"]["Acknolegement"])
            if self.Parameters["TCP"].get("CheckSumTCP"):
                self.Packet[TCP].chksum = int(self.Parameters["TCP"]["CheckSumTCP"])
            if self.Parameters["TCP"].get("Urgent"):
                self.Packet[TCP].urgptr = int(self.Parameters["TCP"]["Urgent"])
            
            flags = 0
            if self.Parameters["TCP"].get("CWR")    : flags += 0b10000000
            if self.Parameters["TCP"].get("ECN")    : flags += 0b01000000
            if self.Parameters["TCP"].get("URG")    : flags += 0b00100000
            if self.Parameters["TCP"].get("ACK")    : flags += 0b00010000
            if self.Parameters["TCP"].get("PSH")    : flags += 0b00001000
            if self.Parameters["TCP"].get("RST")    : flags += 0b00000100
            if self.Parameters["TCP"].get("SYN")    : flags += 0b00000010
            if self.Parameters["TCP"].get("FIN")    : flags += 0b00000001
            self.Packet[TCP].flags = flags

            payload = self.Parameters["TCP"].get('DataTCP', "")

        if self.Parameters["IP"]['Protocol'] == "UDP":
            self.Packet[IP].proto = 17
            self.Packet = self.Packet/UDP()
            if self.Parameters["UDP"].get("Source"):
                self.Packet[UDP].sport = int(self.Parameters["UDP"]["Source"])
            if self.Parameters["UDP"].get("Destination"):
                self.Packet[UDP].dport = int(self.Parameters["UDP"]["Destination"])
            if self.Parameters["UDP"].get("Length"):
                self.Packet[UDP].len = int(self.Parameters["UDP"]["Length"])
            if self.Parameters["UDP"].get("CheckSumUDP"):
                self.Packet[UDP].chksum = int(self.Parameters["UDP"]["CheckSumUDP"])
            
            payload = self.Parameters["UDP"].get('DataUDP', "")

        if self.Parameters["IP"]['Protocol'] == "ICMP":
            self.Packet[IP].proto = 1
            self.Packet = self.Packet/ICMP()
            if self.Parameters["ICMP"].get("TypeICMP") == "EchoRequest":
                self.Packet[ICMP].type = 8
            elif self.Parameters["ICMP"].get("TypeICMP") == "EchoReply":
                self.Packet[ICMP].type = 0
            if self.Parameters["ICMP"].get("CheckSumICMP"):
                self.Packet[ICMP].chksum = int(self.Parameters["ICMP"]["CheckSumICMP"])
            
            payload = self.Parameters["ICMP"].get('DataICMP', "")

        if payload != None:
            self.Packet = self.Packet/payload
    
    def SendPacket(self, interface : str):
        sendp(Ether()/self.Packet, return_packets=True, verbose=True, iface = interface)
    
    def UpdateCheckSum(self, protocol : str = "IP"):      
        if protocol == "IP" or protocol == "Empty":
            del self.Packet.chksum
            self.Packet = self.Packet.__class__(bytes(self.Packet))
            return str(self.Packet.chksum)
        elif protocol == "TCP":
            del self.Packet[TCP].chksum
            self.Packet[TCP] = self.Packet[TCP].__class__(bytes(self.Packet[TCP]))
            return str(self.Packet[TCP].chksum)
        elif protocol == "UDP":
            del self.Packet[UDP].chksum
            self.Packet[UDP] = self.Packet[UDP].__class__(bytes(self.Packet[UDP]))
            return str(self.Packet[UDP].chksum)
        elif protocol == "ICMP":
            del self.Packet[ICMP].chksum
            self.Packet[ICMP] = self.Packet[ICMP].__class__(bytes(self.Packet[ICMP]))
            return str(self.Packet[ICMP].chksum)
        return ""
              
    def GetInterfaces(self):
        return self.Interfaces

    def GetPacket(self):
        return hexdump(self.Packet, dump=True)