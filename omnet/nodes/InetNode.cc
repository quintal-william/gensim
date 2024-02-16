#include <vector>
#include <cstring>
#include <queue>

#include "inet/applications/tcpapp/TcpAppBase.h"
#include "inet/common/lifecycle/LifecycleOperation.h"
#include "inet/common/lifecycle/NodeStatus.h"
#include "inet/applications/base/ApplicationPacket_m.h"
#include "inet/common/ModuleAccess.h"
#include "inet/common/TagBase_m.h"
#include "inet/common/TimeTag_m.h"
#include "inet/common/lifecycle/ModuleOperations.h"
#include "inet/common/packet/Packet.h"
#include "inet/common/packet/chunk/ByteCountChunk.h"
#include "inet/common/packet/chunk/BytesChunk.h"
#include "inet/networklayer/common/L3AddressResolver.h"
#include "../NetworkAnalyzerMessage_m.h"

using namespace inet;

namespace nsim {

class InetSendApp : public TcpAppBase
{
  protected:
    cMessage *timeoutMsg = nullptr;

  protected:
    virtual void handleStartOperation(LifecycleOperation *operation) override;
    virtual void handleStopOperation(LifecycleOperation *operation) override;
    virtual void handleCrashOperation(LifecycleOperation *operation) override;

    virtual int numInitStages() const override { return NUM_INIT_STAGES; }
    virtual void initialize(int stage) override;
    virtual void finish() override;
    virtual void refreshDisplay() const override;

    virtual Packet *createDataPacket(long sendBytes);

    virtual void handleTimer(cMessage *msg) override;
    virtual void socketClosed(TcpSocket *socket) override;
    virtual void socketFailure(TcpSocket *socket, int code) override;

  public:
    void sendData(long numBytes);
    InetSendApp() {}
    virtual ~InetSendApp();
};

Define_Module(InetSendApp);

InetSendApp::~InetSendApp()
{
  cancelAndDelete(timeoutMsg);
}

void InetSendApp::initialize(int stage)
{
  TcpAppBase::initialize(stage);
  if (stage == INITSTAGE_LOCAL) {
    timeoutMsg = new cMessage("timer");
  }
}

void InetSendApp::handleStartOperation(LifecycleOperation *operation)
{
  if (simTime() <= 0) {
    scheduleAt(0, timeoutMsg);
  }
}

void InetSendApp::handleStopOperation(LifecycleOperation *operation)
{
  cancelEvent(timeoutMsg);
  if (socket.isOpen())
    close();
  delayActiveOperationFinish(2);
}

void InetSendApp::handleCrashOperation(LifecycleOperation *operation)
{
  cancelEvent(timeoutMsg);
  if (operation->getRootModule() != getContainingNode(this))
    socket.destroy();
}

void InetSendApp::handleTimer(cMessage *msg)
{
  connect();
}

void InetSendApp::sendData(long numBytes)
{
  Enter_Method("InetNodeMessageProcessor calling InetSendApp's send method");
  EV_INFO << "sending data with " << numBytes << " bytes\n";
  sendPacket(createDataPacket(numBytes));
}

Packet *InetSendApp::createDataPacket(long sendBytes)
{
  Ptr<Chunk> payload = makeShared<ByteCountChunk>(B(sendBytes));
  payload->addTag<CreationTimeTag>()->setCreationTime(simTime());
  Packet *packet = new Packet("data1");
  packet->insertAtBack(payload);
  return packet;
}

void InetSendApp::socketClosed(TcpSocket *socket)
{
  TcpAppBase::socketClosed(socket);
  cancelEvent(timeoutMsg);
  if (operationalState == State::STOPPING_OPERATION && !this->socket.isOpen())
    startActiveOperationExtraTimeOrFinish(-1);
}

void InetSendApp::socketFailure(TcpSocket *socket, int code)
{
  TcpAppBase::socketFailure(socket, code);
  cancelEvent(timeoutMsg);
}

void InetSendApp::finish()
{
  EV << getFullPath() << ": received " << bytesRcvd << " bytes in " << packetsRcvd << " packets\n";
  recordScalar("bytesRcvd", bytesRcvd);
  recordScalar("bytesSent", bytesSent);
}

void InetSendApp::refreshDisplay() const
{
  TcpAppBase::refreshDisplay();
  std::ostringstream os;
  os << TcpSocket::stateName(socket.getState()) << "\nsent: " << bytesSent << " bytes\nrcvd: " << bytesRcvd << " bytes";
  getDisplayString().setTagArg("t", 0, os.str().c_str());
}









class InetNodeMessageProcessor : public cSimpleModule, public cListener {
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
  virtual void receiveSignal(cComponent *source, simsignal_t signalID, const SimTime &t, cObject *details) override;
  InetSendApp *getSendApp(std::string connectAddress);
  std::queue<NetworkAnalyzerMessage *> messageQueue;
};

Define_Module(InetNodeMessageProcessor);

void InetNodeMessageProcessor::initialize() {
  getSimulation()->getSystemModule()->subscribe("rtt", this);
  EV << "Initialized Message Processor" << endl;
}

InetSendApp *InetNodeMessageProcessor::getSendApp(std::string connectAddress) {
  cModule *parentModule = getParentModule();
  if (parentModule) {
    int appArraySize = parentModule->par("numApps").intValue();
    for (int i = 0; i < appArraySize; ++i) {
      cModule *appModule = parentModule->getSubmodule("app", i);
      if (appModule) {
        if (appModule->hasPar("connectAddress")) {
          std::string hostConnectAddress = appModule->par("connectAddress").stringValue();
          if (connectAddress == hostConnectAddress) {
            return check_and_cast<InetSendApp *>(appModule);
          }
        }
      }
    }
  }
  return nullptr;
}

void InetNodeMessageProcessor::receiveSignal(cComponent *source, simsignal_t signalID, const SimTime &t, cObject *details) {
  if (!messageQueue.empty()) {
    cMessage *message = messageQueue.front();
    messageQueue.pop();
    send(message, "out");
  }
}

void InetNodeMessageProcessor::handleMessage(cMessage *msg) {
  if (dynamic_cast<NetworkAnalyzerMessage *>(msg)) {
    NetworkAnalyzerMessage *message = check_and_cast<NetworkAnalyzerMessage *>(msg);
    InetSendApp *app = getSendApp(message->getDestination());
    if (app != nullptr) {
      app->sendData(message->getSize());
      messageQueue.push(message);
    }
  } else {
    delete msg;
  }
}

}
