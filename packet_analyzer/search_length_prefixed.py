print(int(b'0x0A',16))

#  TODO after getting wireshark captures JSON
#  Fetch payload from packet <-- I can modularise this out :)
#  For every packet, Loop through every field
#  For every field, if boundary_type is length_prefix, try to parse packet, otherwise suggest to use a different strategy.
#  Parse Header and Footer to chip off excessive bytes.
#  Now, parse every fixed length field bw Hdr and Ftr
#  When a variable length field is encountered, check its prefix bytes.
#  Jump back those many bytes, read those many bytes and typecast the length into int.
#  If prefix bytes are included, jump those bytes before reading.
#  Continue parsing other fixed bytes until footer.
#  If everything goes right, print Packet found! and display all fields.