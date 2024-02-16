#include <omnetpp.h>
#include <filesystem>
#include <iostream>
#include <fstream>
#include <vector>
#include "json.hpp"
#include "NetworkAnalyzerMessage_m.h"

using namespace omnetpp;

namespace nsim {

class NetworkAnalyzer : public cSimpleModule {
protected:
  virtual void initialize() override;
  virtual void handleMessage(cMessage *msg) override;
  virtual void finish() override;
  void processJsonTrafficFile(const char* filePath);
  void processXmlTrafficFile(const char* filePath);
  void createMessage(
    const std::string& id,
    const std::string& source,
    const std::string& destination,
    int size,
    double time
  );
  const char* jsonFilePath = "./traffic.json";
  const char* xmlFilePath = "./traffic.xml";
  const char* outFilePath = "./results/traffic.json";
  std::vector<NetworkAnalyzerMessage*> messages;
};

Define_Module(NetworkAnalyzer);

void NetworkAnalyzer::initialize() {
  std::ifstream jsonFile(jsonFilePath);
  if (jsonFile) {
    EV << "Found JSON traffic file, processing..." << endl;
    processJsonTrafficFile(jsonFilePath);
    return;
  }

  std::ifstream xmlFile(xmlFilePath);
  if (xmlFile) {
    EV << "Found XML traffic file, processing..." << endl;
    processXmlTrafficFile(xmlFilePath);
    return;
  }

  EV << "Could not find JSON or XML traffic file" << endl;
  EV << "Initialized Network Analyzer" << endl;
}

void NetworkAnalyzer::processJsonTrafficFile(const char* filePath) {
  std::ifstream file(filePath);
  nlohmann::json jsonData;
  file >> jsonData;

  if (jsonData.contains("arrivals") && jsonData["arrivals"].is_array()) {
    for (const auto& arrival : jsonData["arrivals"]) {
      if (!(arrival.contains("id") && arrival["id"].is_string())) {
        EV << "Arrival skipped: 'id' not found or is not a string" << endl;
        continue;
      }

      if (!(arrival.contains("source") && arrival["source"].is_string())) {
        EV << "Arrival skipped: 'source' not found or is not a string" << endl;
        continue;
      }

      if (!(arrival.contains("destination") && arrival["destination"].is_string())) {
        EV << "Arrival skipped: 'destination' not found or is not a string" << endl;
        continue;
      }

      if (!(arrival.contains("size") && arrival["size"].is_number_integer())) {
        EV << "Arrival skipped: 'size' not found or is not an integer" << endl;
        continue;
      }

      if (!(arrival.contains("time") && arrival["time"].is_number_float())) {
        EV << "Arrival skipped: 'time' not found or is not a float" << endl;
        continue;
      }

      std::string id = arrival["id"];
      std::string source = arrival["source"];
      std::string destination = arrival["destination"];
      int size = arrival["size"];
      double time = arrival["time"];
      createMessage(id, source, destination, size, time);
    }
  } else {
    EV << "Invalid JSON traffic file: 'arrivals' key not found or is not an array" << endl;
  }
}

void NetworkAnalyzer::processXmlTrafficFile(const char* filePath) {
  cXMLElement* xml = getEnvir()->getXMLDocument(filePath, nullptr);
  cXMLElement* arrivals = xml->getFirstChildWithTag("arrivals");
  if (arrivals) {
    for (cXMLElement* arrival = arrivals->getFirstChildWithTag("arrival"); arrival; arrival = arrival->getNextSiblingWithTag("arrival")) {
      const char* id = arrival->getAttribute("id");
      const char* source = arrival->getAttribute("source");
      const char* destination = arrival->getAttribute("destination");
      const char* sizeAttr = arrival->getAttribute("size");
      const char* timeAttr = arrival->getAttribute("time");
      char* endPtr;

      if (!id) {
        EV << "Arrival skipped: 'id' not found" << endl;
        continue;
      }

      if (!source) {
        EV << "Arrival skipped: 'source' not found" << endl;
        continue;
      }

      if (!destination) {
        EV << "Arrival skipped: 'destination' not found" << endl;
        continue;
      }

      if (!sizeAttr) {
        EV << "Arrival skipped: 'size' not found" << endl;
        continue;
      }

      int size = strtol(sizeAttr, &endPtr, 10);
      if (*endPtr != '\0') {
        EV << "Arrival skipped: size '" << sizeAttr <<"' is not a valid integer";
        continue;
      }

      if (!timeAttr) {
        EV << "Arrival skipped: 'time' not found" << endl;
        continue;
      }

      double time = strtod(timeAttr, &endPtr);
      if (*endPtr != '\0') {
        EV << "Arrival skipped: time '" << timeAttr <<"' is not a valid float";
        continue;
      }

      createMessage(id, source, destination, size, time);
    }
  } else {
    EV << "Invalid XML traffic file: 'arrivals' tag was not found" << endl;
  }
}

void NetworkAnalyzer::createMessage(
  const std::string& id,
  const std::string& source,
  const std::string& destination,
  int size,
  double time
) {
  NetworkAnalyzerMessage *message = new NetworkAnalyzerMessage(id.c_str());
  message->setId(id.c_str());
  message->setSource(source.c_str());
  message->setDestination(destination.c_str());
  message->setSize(size);

  scheduleAt(time, message);
  EV << "Scheduled message: " << id << endl;
}

void NetworkAnalyzer::handleMessage(cMessage *msg) {
  if (msg->isSelfMessage()) {
    send(msg, "out");
  } else if (dynamic_cast<NetworkAnalyzerMessage *>(msg)) {
    NetworkAnalyzerMessage *message = check_and_cast<NetworkAnalyzerMessage *>(msg);
    messages.push_back(message);
  } else {
    delete msg;
  }
}

void NetworkAnalyzer::finish() {
  nlohmann::json jsonData;
  for (const NetworkAnalyzerMessage *message : messages) {
    nlohmann::json jsonMessage;
    jsonMessage["id"] = message->getId();
    jsonMessage["source"] = message->getSource();
    jsonMessage["destination"] = message->getDestination();
    jsonMessage["size"] = message->getSize();
    jsonMessage["timeEntry"] = std::to_string(message->getTimeEntry().dbl());
    jsonMessage["timeExit"] = std::to_string(message->getTimeExit().dbl());
    jsonData.push_back(jsonMessage);
    delete message;
  }

  std::ofstream file;
  file.open(outFilePath, std::ofstream::out | std::ofstream::trunc);
  file << jsonData.dump(4);
  file.close();
}

}
