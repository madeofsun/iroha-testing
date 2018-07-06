import grpc

from proto import proposal_pb2
from proto import ordering_pb2
from proto import ordering_pb2_grpc
from proto import loader_pb2
from proto import loader_pb2_grpc
from proto import endpoint_pb2
from proto import endpoint_pb2_grpc
from proto import yac_pb2_grpc
from proto import yac_pb2
from proto import block_pb2
from proto import queries_pb2

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

### Requests

def sendTransaction(host, transaction):
  channel = grpc.insecure_channel(host)
  stub = endpoint_pb2_grpc.CommandServiceStub(channel)
  return stub.Torii(transaction)

def sendGetStatus(host, request):
  channel = grpc.insecure_channel(host)
  stub = endpoint_pb2_grpc.CommandServiceStub(channel)
  return stub.Status(request)

def sendQuery(host, query):
  channel = grpc.insecure_channel(host)
  stub = endpoint_pb2_grpc.QueryServiceStub(channel)
  return stub.Find(query)

def sendRelayedTransaction(OS_host, transaction):
  channel = grpc.insecure_channel(OS_host)
  stub = ordering_pb2_grpc.OrderingServiceTransportGrpcStub(channel)
  return stub.onTransaction(transaction)

def sendProposal(host, proposal):
  channel = grpc.insecure_channel(host)
  stub = ordering_pb2_grpc.OrderingGateTransportGrpcStub(channel)
  return stub.onProposal(proposal)

def sendVote(host, vote):
  channel = grpc.insecure_channel(host)
  stub = yac_pb2_grpc.YacStub(channel)
  return stub.SendVote(vote)

def sendCommit(host, commit):
  channel = grpc.insecure_channel(host)
  stub = yac_pb2_grpc.YacStub(channel)
  return stub.SendCommit(commit)

def sendReject(host, reject):
  channel = grpc.insecure_channel(host)
  stub = yac_pb2_grpc.YacStub(channel)
  return stub.SendReject(reject)

def sendLoadBlockS(host, request):
  channel = grpc.insecure_channel(host)
  stub = loader_pb2_grpc.LoaderStub(channel)
  return stub.retrieveBlocks(request)

def sendLoadBlock(host, request):
  channel = grpc.insecure_channel(host)
  stub = loader_pb2_grpc.LoaderStub(channel)
  return stub.retrieveBlock(request)


### Forging stuff

### Send proposal from file (JSON) to hosts
def proposalSender(proposal_filename, hosts):
  with open(proposal_filename, 'r') as f:
    proposal = Parse(f.read(), proposal_pb2.Proposal())

  print(MessageToJson(proposal))

  for host in hosts:
    sendProposal(host, proposal)

### Send request to peer to download all blocks
def syncSender(host):
  for item in sendLoadBlockS(host, loader_pb2.BlocksRequest(height=0)):
    print(MessageToJson(item))


### Send transaction from file (JSON) to peer 
def transactionSender(filename, host):
  with open(filename, 'r') as f:
    transaction = Parse(f.read(), block_pb2.Transaction())
  sendTransaction(host, transaction)

def commitSender(filename, host):
  with open(filename, 'r') as f:
    vote = Parse(f.read(), yac_pb2.Commit())
  sendCommit(host, vote)

def relaedTxSender(filename, host):
  with open(filename, 'r') as f:
    transaction = Parse(f.read(), block_pb2.Transaction())
  sendRelayedTransaction(host, transaction)

def querySeder(filename, host):
  with open(filename, 'r') as f:
    query = Parse(f.read(), queries_pb2.Query())
  result = sendQuery(host, query)
  print(MessageToJson(result))


if __name__ == '__main__':

  querySeder('input/q.json', '192.168.64.145:50052')

  #proposalSender('input/proposal.json', hosts = ['192.168.64.145:10002'])

  #transactionSender('input/transaction.json', '192.168.64.145:50053')
  #relaedTxSender('input/transaction.json', '192.168.64.145:10001')

  #commitSender('input/vote.json','192.168.64.145:10001')

  # proposalSender('input/proposal.json', hosts = [
  #    '192.168.64.145:10001',
  #    '192.168.64.145:10002',
  #    '192.168.64.145:10003',
  #    '192.168.64.145:10004'])
