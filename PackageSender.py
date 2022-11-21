import json

import psutil

from scapy.layers.inet import IP, UDP, TCP, ICMP, Ether
from scapy.all import hexdump, sendp


# SCAPY_DEFAULT_self.PackageS = {
#     "IP": IP(
#             version =int(self.Package_DEFAULTS["IP"]["version"]),
#             ihl     =int(self.Package_DEFAULTS["IP"]["IHL"   ]),
#             len     =int(self.Package_DEFAULTS["IP"]["length"]),
#             id      =int(self.Package_DEFAULTS["IP"]["ID"    ]),
#             frag    =int(self.Package_DEFAULTS["IP"]["offset"]),
#             ttl     =int(self.Package_DEFAULTS["IP"]["TTL"   ]),
#             proto   =int(self.Package_DEFAULTS["IP"]["prot"  ]),
#             src     =self.Package_DEFAULTS["IP"]["ip_src"],
#             dst     =self.Package_DEFAULTS["IP"]["ip_dst"]
#              ),
#     "TCP": TCP(
#             sport   =int(self.Package_DEFAULTS["TCP"]["frm_src_port"]),
#             dport   =int(self.Package_DEFAULTS["TCP"]["frm_dst_port"]),
#             seq     =int(self.Package_DEFAULTS["TCP"]["frm_seq"     ]),
#             ack     =int(self.Package_DEFAULTS["TCP"]["frm_ack"     ]),
#             dataofs =int(self.Package_DEFAULTS["TCP"]["frm_offset"  ]),
#             window  =int(self.Package_DEFAULTS["TCP"]["frm_window"  ]),
#             urgptr  =int(self.Package_DEFAULTS["TCP"]["frm_up"      ])
#     ),
#     "UDP": UDP(
#             sport   =int(self.Package_DEFAULTS["UDP"]["src_port"]),
#             dport   =int(self.Package_DEFAULTS["UDP"]["dst_port"]),
#             len     =int(self.Package_DEFAULTS["UDP"]["length"  ]),
#     ),
#     "ICMP": ICMP(
#             type    =self.Package_DEFAULTS["ICMP"]["type"  ]
#     )
# }


class PackageSender():
    def __init__(self):
        self.Package = IP()
        self.Parameters = {}
        self.Interfaces = psutil.net_if_addrs()
    
    def FormPackage(self, filename : str = None, params = None):
        del self.Package
        self.Package = IP()
        self.Package[IP].version = 4 #?
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
            self.Package[IP].src = self.Parameters["IP"].get("Source")
        if self.Parameters["IP"].get("Destination"): 
            self.Package[IP].dst = self.Parameters["IP"].get("Destination")

        if self.Parameters["IP"].get("Header"): 
            self.Package[IP].ihl = int(self.Parameters["IP"].get("Header"))
        if self.Parameters["IP"].get("Identification"): 
            self.Package[IP].id = int(self.Parameters["IP"].get("Identification"))
        if self.Parameters["IP"].get("CheckSumIP"):
             self.Package[IP].chksum = int(self.Parameters["IP"].get("CheckSumIP"))
        if self.Parameters["IP"].get("TotalLength"):
             self.Package[IP].len = int(self.Parameters["IP"].get("TotalLength"))
        if self.Parameters["IP"].get("TTL"):
             self.Package[IP].ttl = int(self.Parameters["IP"].get("TTL"))

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
        self.Package[IP].tos = TOS

        flags = 0
        if self.Parameters["IP"].get("Offset"):
             self.Package[IP].frag = int(self.Parameters["IP"].get("Offset"))

        if self.Parameters["IP"].get('Fragmentation'):
            if "Reserved" in self.Parameters["IP"].get("Fragmentation"):
                flags += 0b100
            if "NoFragment" in self.Parameters["IP"].get("Fragmentation"):
                flags += 0b010
            if "MoreFragment" in self.Parameters["IP"].get("Fragmentation"):
                flags += 0b001
        self.Package[IP].flags = flags


        payload = ""
        if self.Parameters["IP"]['Protocol'] == "TCP":
            self.Package[IP].proto = 6
            self.Package = self.Package/TCP()

            if self.Parameters["TCP"].get("Source"):
                self.Package[TCP].sport = int(self.Parameters["TCP"]["Source"])
            if self.Parameters["TCP"].get("Destination"):
                self.Package[TCP].dport = int(self.Parameters["TCP"]["Destination"])
            if self.Parameters["TCP"].get("TCPOffset"):
                self.Package[TCP].dataofs = int(self.Parameters["TCP"]["TCPOffset"])
            if self.Parameters["TCP"].get("Window"):
                self.Package[TCP].window = int(self.Parameters["TCP"]["Window"])
            if self.Parameters["TCP"].get("Sequence"):
                self.Package[TCP].seq = int(self.Parameters["TCP"]["Sequence"])
            if self.Parameters["TCP"].get("Acknolegement"):
                self.Package[TCP].ack = int(self.Parameters["TCP"]["Acknolegement"])
            if self.Parameters["TCP"].get("CheckSumTCP"):
                self.Package[TCP].chksum = int(self.Parameters["TCP"]["CheckSumTCP"])
            if self.Parameters["TCP"].get("Urgent"):
                self.Package[TCP].urgptr = int(self.Parameters["TCP"]["Urgent"])
            
            flags = 0
            if self.Parameters["TCP"].get("URG")    : flags += 0b00100000
            if self.Parameters["TCP"].get("ACK")    : flags += 0b00010000
            if self.Parameters["TCP"].get("PSH")    : flags += 0b00001000
            if self.Parameters["TCP"].get("RST")    : flags += 0b00000100
            if self.Parameters["TCP"].get("SYN")    : flags += 0b00000010
            if self.Parameters["TCP"].get("FIN")    : flags += 0b00000001
            self.Package[TCP].flags = flags

            payload = self.Parameters["TCP"].get('DataTCP', "")

        if self.Parameters["IP"]['Protocol'] == "UDP":
            self.Package[IP].proto = 17
            self.Package = self.Package/UDP()
            if self.Parameters["UDP"].get("Source"):
                self.Package[UDP].sport = int(self.Parameters["UDP"]["Source"])
            if self.Parameters["UDP"].get("Destination"):
                self.Package[UDP].dport = int(self.Parameters["UDP"]["Destination"])
            if self.Parameters["UDP"].get("Length"):
                self.Package[UDP].len = int(self.Parameters["UDP"]["Length"])
            if self.Parameters["UDP"].get("CheckSumUDP"):
                self.Package[UDP].chksum = int(self.Parameters["UDP"]["CheckSumUDP"])
            
            payload = self.Parameters["UDP"].get('DataUDP', "")

        if self.Parameters["IP"]['Protocol'] == "ICMP":
            self.Package[IP].proto = 1
            self.Package = self.Package/ICMP()
            if self.Parameters["ICMP"].get("TypeICMP") == "EchoRequest":
                self.Package[ICMP].type = 8
            elif self.Parameters["ICMP"].get("TypeICMP") == "EchoReply":
                self.Package[ICMP].type = 0
            if self.Parameters["ICMP"].get("CheckSumICMP"):
                self.Package[ICMP].chksum = int(self.Parameters["ICMP"]["CheckSumICMP"])
            
            payload = self.Parameters["ICMP"].get('DataICMP', "")

        if payload != None:
            self.Package = self.Package/payload
    
    def SendPackage(self, interface : str):
        sendp(Ether()/self.Package, return_packets=True, verbose=True, iface = interface)
    
    def UpdateCheckSum(self, protocol : str = "IP"):      
        if protocol == "IP" or protocol == "Empty":
            del self.Package.chksum
            self.Package = self.Package.__class__(bytes(self.Package))
            return str(self.Package.chksum)
        elif protocol == "TCP":
            del self.Package[TCP].chksum
            self.Package[TCP] = self.Package[TCP].__class__(bytes(self.Package[TCP]))
            return str(self.Package[TCP].chksum)
        elif protocol == "UDP":
            del self.Package[UDP].chksum
            self.Package[UDP] = self.Package[UDP].__class__(bytes(self.Package[UDP]))
            return str(self.Package[UDP].chksum)
        elif protocol == "ICMP":
            del self.Package[ICMP].chksum
            self.Package[ICMP] = self.Package[ICMP].__class__(bytes(self.Package[ICMP]))
            return str(self.Package[ICMP].chksum)
        return ""
              
    def GetInterfaces(self):
        return self.Interfaces

    def GetPackage(self):
        return hexdump(self.Package, dump=True)