# Shingeki no Iroha


Repository with configuration for testing environment and scripts used for testing:
  ```
  https://github.com/madeofsun/iroha-testing
  ```

## Testing environment

Testing environment contained 4 peers run on single machine in docker containers.

To deploy, enter `env_config` directory.
Modify IP addresses of peers in `genesis_block` to hosts external IP address.
Run `./deploy.sh` (requires gnome-terminal).

## Message forging

`forge.py` - contains functions to send specific to Iroha gRPC messages. gRPC message can be parsed from JSON file.

Dependencies:
```
$ pip install grpcio-tools googleapis-common-protos
```

## Message intercepting

`proxy.py` - allows to intercept incoming gRPC messages for specific peer. What to do with the message can be specified in correspoding methods inside `proxy.py`. By default, messages are simply redirected using functions from `forge.py`.
How to use:


    python proxy.py config_file

Example of config file:
```
{
  "fake_address": "0.0.0.0",
  "fake_port": "5501",
  "real_address": "192.168.64.145",
  "torii_port": "50051",
  "yac_port": "10001",
  "send_to_address": "127.0.0.1",
  "log_file": "logs/proxy1.log"
}
```

`fake_address` - address the proxy should run on
`fake_port` - port the proxy should run on
`real_address` - address of original destination
`torii_port` - original port for user's transactions/queries
`yac_port` - original port for peer communication
`send_to_address` - address to send tampered requests to
`log_file` - file to save requests and responses as JSON


## Found vulnerabilities


### 1. User’s transaction replay 

* Each transaction is remembered by hash, but: 1) when node is rebooted - cache is purged; 2) cache can be overflown. 
* The check is applied only at Torii.
* Transaction’s time interval of validity is too large (approx 24 hours), so there is increased probability of successful replay attack.

**CWE-287: Improper Authentication**
**CWE-294: Authentication Bypass by Capture-replay**
**CVSS v.3 Base Score 6.1 with Vector AV:N/AC:H/PR:N/UI:R/S:C/C:N/I:H/A:N**

*How to perform:*

Take committed transaction from block_store, save transaction in JSON file and use `transactionSender` function in `forge.py`.


### 2. User's query replay 
* Each transaction is remembered by hash, but: 1) when node is rebooted - cache is purged; 2) cache can be overflown.
* Replayed query can be served by another peer.
* Query’s time interval of validity is too large (approx 24 hours), so there is increased probability of successful replay attack.

**CWE-287: Improper Authentication
CWE-294: Authentication Bypass by Capture-replay
CVSS v.3 Base Score 3.4 with Vector AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:N/A:N**

*How to perform:*

Use `proxy.py` to capture query as JSON and save it in file, then use `querySender` function in `forge.py`.

### 3. Query/txStatus response forgery/replaying/tampering
* Response is not authenticated. As the result, client can receive inappropriate data and make a wrong decision based on that data.

**CWE-345: Insufficient Verification of Data Authenticity**
**CVSS v.3 Base Score 6.1 with Vector  AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:N/A:N**


How to perform:

Use `proxy.py` for peer you are interested in and define what should be done with response in `QueriesGate.Find` or `TransactionsGate.Status` methods.

Example for `tx_status` tampering:

```
### Torii proxy

class TransactionsGate(endpoint_pb2_grpc.CommandServiceServicer):

  # Handler for transaction's status request
    
  def Status(self, request, context):
    log('Get status', MessageToJson(request))
    
    # Redirect to real peer 
    response = sendGetStatus(TORII_SEND_TO_ADDRESS, request)
    log('Status response', MessageToJson(response))

    # Transaction status is changed in response
    response.tx_status = endpoint_pb2.NOT_RECEIVED
    return response
```


### 4. Transaction replaying on the path from OG to OS
* Transaction that already applied to the ledger is not recognized and filtered.
* Transaction sender is not authenticated.

**CWE-345: Insufficient Verification of Data Authenticity**
**CVSS v.3 Base Score 6.8 with Vector AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:N**

*How to perform:*

Take transaction committed transaction from block_store, save transaction in JSON file and use `relayedTxSender` function in `forge.py`.


### 5. Proposal forgery
* Replayed transactions inside proposal are not filtered.
* Transaction’s time interval is too large (approx 24 hours).
* Proposal sender is not authenticated.
* If forged proposal send to the network not from Ordering Service with valid height and corresponding block applied, then, when the next proposal from Ordering Service comes, it is ignored by peers because height value is low (but height of the next proposal is still incremented, so it will be processed). So the attacker can block original proposals by issuing his own ones.


**CWE-345: Insufficient Verification of Data Authenticity**
**CWE-821: Incorrect Synchronization**
**CVSS v.3 Base Score 8.5 with Vector AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L**

*How to perform:*

Use `proxy.py` for any node to capture some proposal as JSON, save it in file and increment height by 1, then use `proposalSender` function in `forge.py`.

### 6. Proposal jamming
* If proposal is not delivered to more than ⅓ of peers, then Ordering Service goes ahead of everyone and new proposal will be put in queue until missed proposal comes, but it will never come.

**CWE-821: Incorrect Synchronization**
**CVSS v.3 Base Score 5.8 with Vector AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:N/A:H**


*How to perform:*

Launch `proxy.py` for ⅓ of peers with modified `OrderingGate.onProposal` method that drops/corrupts proposal.

Example:

```
class OrderingGate(ordering_pb2_grpc.OrderingGateTransportGrpcServicer):
  
  # Proposal handler
  
  def onProposal(self, request, context):
    log('Proposal', MessageToJson(request))
    # make poroposal obsolete
    request.height -= 1 
    return sendProposal(YAC_SEND_TO_ADDRESS, request)
```


### 7. Error in vote message handling
* If peer receives serialized Commit instead of Vote for SendVote() gRPC call, it crashes.

```
#[2018-07-05 13:58:08.602811208][th:88][error] YacPbConverter::deserializeVote Cannot build vote hash block signature: Signature Builder: [[Public key has wrong size, passed size: 0. Expected size: 32 ]]
#[2018-07-05 13:58:08.604775737][th:88][error] YacPbConverter::deserializeVote Cannot build vote signature: Signature Builder: [[Public key has wrong size, passed size: 0. Expected size: 32 ]]
```

**CWE-248: Uncaught Exception
CVSS v.3 Base Score 8.6 with Vector AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H**


How to perform:
Launch `proxy.py` for some peer with modified Commit handler.

Example:

```
def SendCommit(self, request, context):
    log('Commit', MessageToJson(request))
    #sendVote(PEERS_REAL_ADDRESS, request) # results in segmentation fault
    return empty_pb2
```

### 8. Sync request forgery/replay
* Requests for block loading do not require authentication.

**CWE-200: Information Exposure
CWE-306: Missing Authentication for Critical Function
CVSS v.3 Base Score 8.6 with Vector
AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N**

*How to perform:*

`syncSender` function in `forge.py` allows to download all committed blocks. 
 















