cfg_dir=`pwd ./`
i=
for i in {1..4}
do
  docker stop iroha$i >> /dev/null;
  docker rm iroha$i >> /dev/null;
  docker stop some-postgres$i >> /dev/null;
  docker rm some-postgres$i >> /dev/null;
  docker volume rm blockstore$i >> /dev/null;
  docker network rm iroha-network$i >> /dev/null;

  docker network create iroha-network$i;
  docker run --name some-postgres$i \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=oneirohatwoiroha \
  --network=iroha-network$i \
  -d postgres:9.5;
done

sleep 5
str="gnome-terminal "
for i in {1..4}
do
cc="docker run -it --name iroha$i \
  -p 5005$i:5005$i \
  -p 1000$i:1000$i \
  --network=iroha-network$i \
  -v $cfg_dir:/opt/iroha_data \
  -v blockstore$i:/tmp/block_store \
  --entrypoint=/usr/bin/irohad hyperledger/iroha:develop --config config$i --genesis_block genesis.block --keypair_name node$i --overwrite-ledger";
str="$str --tab -e \"$cc\"";
done

/bin/bash -c "$str >> /dev/null"
