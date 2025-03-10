
#
# Pre-buit filters for patches
#

mpk_a_filter = PortFilter(mpk_port_a)
mpk_b_filter = PortFilter(mpk_port_b)
pk5_filter   = PortFilter(mpk_midi) >> ChannelFilter(3)
q49_filter   = PortFilter(q49_midi)

# -------------------------------
