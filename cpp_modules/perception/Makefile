CXX = g++
CXXFLAGS = -std=c++17 -Wall -O3 -fPIC -shared
TARGET = libperception.so
SOURCE = perception.cpp

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)

clean:
	rm -f $(TARGET)

.PHONY: all clean
