message NetworkAnalyzerMessage {
  string id;
  string source;
  string destination;
  int size;
  simtime_t timeEntry;
  simtime_t timeExit;
}
