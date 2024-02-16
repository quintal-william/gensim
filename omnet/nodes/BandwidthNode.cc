#include <omnetpp.h>
#include <algorithm>
#include "../NetworkAnalyzerMessage_m.h"

using namespace omnetpp;

namespace nsim {

class BandwidthNode : public cSimpleModule {
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
  double bandwidth;
};

Define_Module(BandwidthNode);

void BandwidthNode::initialize() {
  bandwidth = par("bandwidth").doubleValue();
  EV << "Initialized Bandwidth Node" << endl;
}

void BandwidthNode::handleMessage(cMessage *msg) {
  if (msg->isSelfMessage()) {
    send(msg, "out");
  } else if (dynamic_cast<NetworkAnalyzerMessage *>(msg)) {
    NetworkAnalyzerMessage *message = check_and_cast<NetworkAnalyzerMessage *>(msg);
    scheduleAt(simTime() + message->getSize() / bandwidth, message);
  } else {
    delete msg;
  }
}

}
