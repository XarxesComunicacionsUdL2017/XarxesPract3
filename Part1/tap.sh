ip link set tap0 down
tunctl -t tap0 -u jaume
ip link set tap0 up
ip addr add 10.0.0.3/24 dev tap0
