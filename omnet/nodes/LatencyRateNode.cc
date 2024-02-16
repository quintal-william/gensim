#include <omnetpp.h>
#include <algorithm>
#include "../NetworkAnalyzerMessage_m.h"

using namespace omnetpp;

namespace nsim {

class LatencyRateNode : public cSimpleModule {
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
  double latency;
  double rate;
  simtime_t previousSendTime;
};

Define_Module(LatencyRateNode);

void LatencyRateNode::initialize() {
    latency = par("latency").doubleValue();
    rate = par("rate").doubleValue();
    previousSendTime = 0;
  EV << "Initialized Latency Rate Node" << endl;
}

void LatencyRateNode::handleMessage(cMessage *msg) {
  if (msg->isSelfMessage()) {
    send(msg, "out");
  } else if (dynamic_cast<NetworkAnalyzerMessage *>(msg)) {
    NetworkAnalyzerMessage *message = check_and_cast<NetworkAnalyzerMessage *>(msg);
    simtime_t time = std::max(simTime() + latency, previousSendTime) + message->getSize() / rate;
    previousSendTime = time;
    scheduleAt(time, message);
  } else {
    delete msg;
  }
}

}
