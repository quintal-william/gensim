package nsim.nodes;

import inet.node.inet.StandardHost;
import inet.applications.contract.IApp;

simple InetSendApp like IApp {
  parameters:
    string localAddress;
    string connectAddress;
    int localPort = default(-1); 
    int connectPort = default(1000);
    int timeToLive = default(-1); // if not -1, set the TTL (IPv4) or Hop Limit (IPv6) field of sent packets to this value
    int dscp = default(-1); // if not -1, set the DSCP (IPv4/IPv6) field of sent packets to this value
    int tos = default(-1); // if not -1, set the Type Of Service (IPv4) / Traffic Class (IPv6) field of sent packets to this value
    @display("i=block/app");
    @lifecycleSupport;
    @signal[connect](type=long);
    @signal[packetSent](type=inet::Packet);
    @signal[packetReceived](type=inet::Packet);
    @statistic[packetReceived](title="packets received"; source=packetReceived; record=count,"sum(packetBytes)","vector(packetBytes)"; interpolationmode=none);
    @statistic[packetSent](title="packets sent"; source=packetSent; record=count,"sum(packetBytes)","vector(packetBytes)"; interpolationmode=none);
    @statistic[endToEndDelay](title="end-to-end delay"; source="dataAge(packetReceived)"; unit=s; record=histogram,weightedHistogram,vector; interpolationmode=none);
  gates:
    input socketIn @labels(TcpCommand/up);
    output socketOut @labels(TcpCommand/down);
}

simple InetNodeMessageProcessor {
  gates:
    input in;
    output out;
}

module InetNode extends StandardHost {
  parameters:
    forwarding = true;
  gates:
    input in;
    output out;
  submodules:
    messageProcessor: InetNodeMessageProcessor;
  connections:
    in --> messageProcessor.in;
    messageProcessor.out --> out;
}
