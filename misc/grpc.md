
# gRPC c++ usage

install
```
$ sudo apt install build-essential autoconf libtool pkg-config libgflags-dev libgtest-dev clang libc++-dev
$ git clone https://github.com/grpc/grpc && cd grpc
$ git submodule update --init
$ make && sudo make install
```

## memo

```
PROTOC    = protoc
CXX       = g++
CXXFLAGS += -std=c++11
CXXFLAGS += `pkg-config --cflags protobuf grpc`
LDFLAGS  += `pkg-config --libs   protobuf grpc grpc++`
LDFLAGS  += -lgrpc++_reflection -ldl  #mac
# LDFLAGS  +=  -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed -ldl #linux

.cc.o:
	$(CXX) $(CXXFLAGS) -c $< -o $@

SERVICE = helloworld
GRPCSRC = $(SERVICE).pb.cc $(SERVICE).grpc.pb.cc
GRPCHDR = $(SERVICE).pb.h  $(SERVICE).grpc.pb.h
GRPCOBJ = $(GRPCSRC:.cc=.o)
SERVERSRC = server.cc
CLIENTSRC = client.cc
SERVEROBJ = $(SERVERSRC:.cc=.o)
CLIENTOBJ = $(CLIENTSRC:.cc=.o)

all: buildproto $(SERVEROBJ) $(CLIENTOBJ)
	$(CXX) $(CXXFLAGS) $(GRPCSRC) $(SERVEROBJ) -o server.out $(LDFLAGS)
	$(CXX) $(CXXFLAGS) $(GRPCSRC) $(CLIENTOBJ) -o client.out $(LDFLAGS)

buildproto: $(SERVICE).proto
	$(PROTOC) --grpc_out=. \
		--plugin=protoc-gen-grpc=`which grpc_cpp_plugin` $(SERVICE).proto
	$(PROTOC) --cpp_out=. $(SERVICE).proto
	make $(GRPCOBJ)

clean:
	rm -f \
		$(SERVICE).pb.h \
		$(SERVICE).pb.cc \
		$(SERVICE).grpc.pb.h \
		$(SERVICE).grpc.pb.cc \
		$(SERVEROBJ) \
		$(CLIENTOBJ) \
		*.o *.out
```


```
#include <iostream>
#include <memory>
#include <string>
#include <grpc++/grpc++.h>
#include "helloworld.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using helloworld::HelloRequest;
using helloworld::HelloReply;
using helloworld::Greeter;

class GreeterClient {
 public:
  GreeterClient(std::shared_ptr<Channel> channel)
      : stub_(Greeter::NewStub(channel)) {}

  std::string SayHello(const std::string& user) {
    HelloRequest request;
    request.set_name(user);
    HelloReply reply;
    ClientContext context;
    Status status = stub_->SayHello(&context, request, &reply);

    if (status.ok()) {
      return reply.message();
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return "RPC failed";
    }
  }

 private:
  std::unique_ptr<Greeter::Stub> stub_;
};

int main(int argc, char** argv) {
  GreeterClient greeter(
    grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials())
  );
  std::string user("world");
  std::string reply = greeter.SayHello(user);
  std::cout << "Greeter received: " << reply << std::endl;
}
```

```
syntax = "proto3";
option java_multiple_files = true;
option java_package = "io.grpc.examples.helloworld";
option java_outer_classname = "HelloWorldProto";
option objc_class_prefix = "HLW";

package helloworld;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
	rpc Test (TestRequest) returns (TestReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}

message TestRequest {
	string name = 1;
}

message TestReply {
	string message = 1;
}
```

```
#include <iostream>
#include <memory>
#include <string>
#include <grpc++/grpc++.h>
#include "helloworld.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using helloworld::HelloRequest;
using helloworld::HelloReply;
using helloworld::TestRequest;
using helloworld::TestReply;
using helloworld::Greeter;

class GreeterServiceImpl final : public Greeter::Service {
  Status SayHello(ServerContext* context, const HelloRequest* request,
                  HelloReply* reply) override {
    reply->set_message(std::string("Hello ") + request->name());
    printf("SayHello\n");
    return Status::OK;
  }
  Status Test(ServerContext* context, const TestRequest* request,
                  TestReply* reply) override {
    reply->set_message(std::string("Test ") + request->name());
    printf("Test\n");
    return Status::OK;
  }
};

void RunServer() {
  std::string server_address("0.0.0.0:50051");
  GreeterServiceImpl service;

  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  server->Wait();
}

int main(int argc, char** argv) {
  RunServer();
}
```
