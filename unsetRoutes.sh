iptables -t nat -D OUTPUT -d $1 -p tcp --dport $2 -j REDIRECT --to-ports $4
iptables -t nat -D PREROUTING -d $1 -p tcp --dport $2 -j REDIRECT --to-ports $4
iptables -t nat -D OUTPUT -d $1 -p tcp --dport $3 -j REDIRECT --to-ports $4
iptables -t nat -D PREROUTING -d $1 -p tcp --dport $3 -j REDIRECT --to-ports $4
