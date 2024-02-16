#include <omnetpp.h>
#include "NetworkAnalyzerMessage_m.h"

using namespace omnetpp;

namespace nsim {

class NetworkEntryPoint : public cSimpleModule {
private:
  std::map<std::string, int> gateMap;
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
};

Define_Module(NetworkEntryPoint);

void NetworkEntryPoint::initialize() {
  for (int i = 0; i < gateSize("out"); i++) {
    cGate *outGate = gate("out", i);
    gateMap[outGate->getPathEndGate()->getOwner()->getFullPath()] = i;
  }
  EV << "Initialized Network Entry Point" << endl;
}

void NetworkEntryPoint::handleMessage(cMessage *msg) {
  if (dynamic_cast<NetworkAnalyzerMessage *>(msg)) {
    NetworkAnalyzerMessage *message = check_and_cast<NetworkAnalyzerMessage *>(msg);
    message->setTimeEntry(simTime());

    std::string modulePath = getFullPath();
    modulePath.resize(modulePath.length() - 5); // Remove "entry" from the module path
    modulePath.append(message->getSource());
    modulePath.append(".messageProcessor");

    send(message, "out", gateMap[modulePath]);
  } else {
    delete msg;
  }
}

}
