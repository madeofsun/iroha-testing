import sys
import time
import json
from subprocess import call
from concurrent import futures

import grpc
from google.protobuf.json_format import MessageToJson
from google.protobuf import empty_pb2

from proto import ordering_pb2_grpc
from proto import ordering_pb2
from proto import yac_pb2_grpc
from proto import yac_pb2
from proto import loader_pb2_grpc
from proto import loader_pb2
from proto import endpoint_pb2_grpc
from proto import endpoint_pb2


from forge import sendTransaction
from forge import sendQuery
from forge import sendGetStatus
from forge import sendRelayedTransaction
from forge import sendProposal
from forge import sendVote
from forge import sendCommit
from forge import sendReject
from forge import sendLoadBlockS
from forge import sendLoadBlock


with open(sys.argv[1], 'r') as f:
  config = json.loads(f.read())


FAKE_ADDRESS = config['fake_address']
FAKE_PORT = config['fake_port']
REAL_ADDRESS = config['real_address']
YAC_PORT = config['yac_port']
TORII_PORT = config['torii_port']
YAC_SEND_TO_ADDRESS = "{}:{}".format(config['send_to_address'], YAC_PORT)
TORII_SEND_TO_ADDRESS = "{}:{}".format(config['send_to_address'], TORII_PORT)
LOG_FILE = config['log_file']

# with open(LOG_FILE, 'w') as f:
#   f.write('')

def log(t, message):
  print(t)
  with open(LOG_FILE, 'a') as f:
    f.write('{} {}\n{}\n'.format(t, time.strftime("[ %H:%M:%S ]", time.gmtime()), message))


### Torii proxy

class TransactionsGate(endpoint_pb2_grpc.CommandServiceServicer):

  def Torii(self, request, context):
    log('Transaction', MessageToJson(request))
    return sendTransaction(TORII_SEND_TO_ADDRESS, request)
  
  def Status(self, request, context):
    log('Get status', MessageToJson(request))
    response = sendGetStatus(TORII_SEND_TO_ADDRESS, request)
    log('Status response', MessageToJson(response))

    # Transaction status can be changed here
    # response.tx_status = endpoint_pb2.NOT_RECEIVED

    return response

  def StatusStream(self, request, context):
    yield empty_pb2


class QueriesGate(endpoint_pb2_grpc.QueryServiceServicer):

  def Find(self, request, context):
    log('Query', MessageToJson(request))
    result = sendQuery(TORII_SEND_TO_ADDRESS, request)
    log('Query result', MessageToJson(result))

    # Query result can be changed here
    print(context.peer())

    return result


### Transaction relay proxy

class OrderingService(ordering_pb2_grpc.OrderingServiceTransportGrpcServicer):

  def onTransaction(self, request, context):
    log('Relayed transaction', MessageToJson(request))
    return sendRelayedTransaction(YAC_SEND_TO_ADDRESS, request)


### Proposal proxy

class OrderingGate(ordering_pb2_grpc.OrderingGateTransportGrpcServicer):

  def onProposal(self, request, context):
    log('Proposal', MessageToJson(request))
    return sendProposal(YAC_SEND_TO_ADDRESS, request)


### Vote/Commit/Reject proxy

class YacGate(yac_pb2_grpc.YacServicer):

  def SendVote(self, request, context):
    log('Vote', MessageToJson(request))
    return sendVote(YAC_SEND_TO_ADDRESS, request)
    # print(context.peer())
  
    # if str(context.peer()).split('.')[-1] == '6':
    #   sendVote(PEERS_REAL_ADDRESS, request)
    # return empty_pb2
  
  def SendCommit(self, request, context):
    log('Commit', MessageToJson(request))
    return sendCommit(YAC_SEND_TO_ADDRESS, request)

    #sendVote(PEERS_REAL_ADDRESS, request) # results in segmentation fault
    #[2018-07-05 13:58:08.602811208][th:88][error] YacPbConverter::deserializeVote Cannot build vote hash block signature: Signature Builder: [[Public key has wrong size, passed size: 0. Expected size: 32 ]]
    #[2018-07-05 13:58:08.604775737][th:88][error] YacPbConverter::deserializeVote Cannot build vote signature: Signature Builder: [[Public key has wrong size, passed size: 0. Expected size: 32 ]]

    #sendReject instead of commit is not a problem

  def SendReject(self, request, context):
    log('Reject', MessageToJson(request))
    return sendReject(YAC_SEND_TO_ADDRESS, request)


### Block loader proxy

class LoaderGate(loader_pb2_grpc.LoaderServicer):

  def retrieveBlocks(self, request, context):
    log('Retrive blockS', MessageToJson(request))
    for item in sendLoadBlockS(YAC_SEND_TO_ADDRESS, request):
      yield item
  
  def retrieveBlock(self, request, context):
    log('Retrive block', MessageToJson(request))
    return sendLoadBlock(YAC_SEND_TO_ADDRESS, request)


def serve():
  proxy = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
  
  endpoint_pb2_grpc.add_QueryServiceServicer_to_server(QueriesGate(), proxy)
  endpoint_pb2_grpc.add_CommandServiceServicer_to_server(TransactionsGate(), proxy)
  ordering_pb2_grpc.add_OrderingGateTransportGrpcServicer_to_server(OrderingGate(), proxy)
  ordering_pb2_grpc.add_OrderingServiceTransportGrpcServicer_to_server(OrderingService(), proxy)
  yac_pb2_grpc.add_YacServicer_to_server(YacGate(), proxy)
  loader_pb2_grpc.add_LoaderServicer_to_server(LoaderGate(), proxy)

  proxy.add_insecure_port("{}:{}".format(FAKE_ADDRESS, FAKE_PORT))
  proxy.start()

  print('Proxy serving on {}:{} for peer {} - Torii at {} and Yac at {}'.format(FAKE_ADDRESS, FAKE_PORT, REAL_ADDRESS, TORII_PORT, YAC_PORT))
  print('Log file is {}'.format(LOG_FILE))

  call(["/bin/bash", "setRoutes.sh", REAL_ADDRESS, TORII_PORT, YAC_PORT, FAKE_PORT])

  try:
    while True:
      time.sleep(60 * 60 * 24)
  except KeyboardInterrupt:
    call(["/bin/bash", "unsetRoutes.sh", REAL_ADDRESS, TORII_PORT, YAC_PORT, FAKE_PORT])
    proxy.stop(0)


if __name__ == '__main__':
  serve()
