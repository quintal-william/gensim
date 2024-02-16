#include <omnetpp.h>
#include "NetworkAnalyzerMessage_m.h"

using namespace omnetpp;

namespace nsim {

class NetworkExitPoint : public cSimpleModule {
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
};

Define_Module(NetworkExitPoint);

void NetworkExitPoint::initialize() {
  EV << "Initialized Network Exit Point" << endl;
}

void NetworkExitPoint::handleMessage(cMessage *msg) {
  if (dynamic_cast<NetworkAnalyzerMessage *>(msg)) {
    NetworkAnalyzerMessage *message = check_and_cast<NetworkAnalyzerMessage *>(msg);
    message->setTimeExit(simTime());
    send(message, "out");
  } else {
    delete msg;
  }
}

}
