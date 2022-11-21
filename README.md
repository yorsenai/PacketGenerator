# PackageGenerator
IP, TCP, UDP and ICMP Package Generator with GUI

The PG has the following functionality:

• Determination of the network cards present and the ability for the user to select the desired card.
• PG provides independent formation of information of link layer packets (Ethernet 802.3):
    o MAC address of the sender;
    o MAC address of the recipient;
    o upper layer protocol type.
• PG allows user to generate any IP, TCP, UDP and ICMP (only Echo request and Echo Reply) packet. User is able to set any value in the field of the corresponding protocol, including the wrong values. It is also possible to enter values into reserved bits of fields, enter an incorrect checksum, etc.
• In the individual protocol fields, the user is able to enter data (TCP, UDP, ICMP).
• It is possible to save the generated packets so that it can be sent later.
• User is able to create queues of packets (for example to perform DOS and flooding attacks).
• Fragmentation is possible too, so user also is able to perform attacks that require port changing.
