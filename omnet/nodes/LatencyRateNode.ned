package nsim.nodes;

simple LatencyRateNode {
	parameters:
		double latency;
		double rate;
	gates:
		input in;
		output out;
}
