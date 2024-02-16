#include <omnetpp.h>
#include <algorithm>
#include "../NetworkAnalyzerMessage_m.h"

using namespace omnetpp;

namespace nsim {

class ConstantDelayNode : public cSimpleModule {
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
  double delay;
};

Define_Module(ConstantDelayNode);

void ConstantDelayNode::initialize() {
  delay = par("delay").doubleValue();
  EV << "Initialized Constant Delay Node" << endl;
}

void ConstantDelayNode::handleMessage(cMessage *msg) {
  if (msg->isSelfMessage()) {
    send(msg, "out");
  } else if (dynamic_cast<NetworkAnalyzerMessage *>(msg)) {
    NetworkAnalyzerMessage *message = check_and_cast<NetworkAnalyzerMessage *>(msg);
    scheduleAt(simTime() + delay, message);
  } else {
    delete msg;
  }
}

}
