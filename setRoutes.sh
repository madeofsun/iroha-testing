iptables -t nat -I OUTPUT -d $1 -p tcp --dport $2 -j REDIRECT --to-ports $4
iptables -t nat -I OUTPUT -d $1 -p tcp --dport $3 -j REDIRECT --to-ports $4
iptables -t nat -I PREROUTING -d $1 -p tcp --dport $2 -j REDIRECT --to-ports $4
iptables -t nat -I PREROUTING -d $1 -p tcp --dport $3 -j REDIRECT --to-ports $4
