# Define compiler and compiler flags
JAVAC = javac
JFLAGS = -g

# Define the Java source files
SOURCES = src/memSim.java src/PageTable.java src/PageTableEntry.java src/PhysicalMemory.java src/TLB.java src/TlbEntry.java

# Define the class files
CLASSES = $(SOURCES:.java=.class)

# Define the executable
EXECUTABLE = memSim

# Default target
all: $(EXECUTABLE)

# Compile Java source files
%.class: %.java
	$(JAVAC) $(JFLAGS) $<

# Build the executable
$(EXECUTABLE): $(CLASSES)
	echo "Main-Class: memSim" > manifest.txt
	jar cvfm $(EXECUTABLE).jar manifest.txt $(CLASSES)
	rm manifest.txt
	echo "#!/bin/bash" > $(EXECUTABLE)
    echo "java -jar $(EXECUTABLE).jar \"\$$@\"" >> $(EXECUTABLE)
	chmod +x $(EXECUTABLE)

# Clean up intermediate files
clean:
	rm -f $(CLASSES) $(EXECUTABLE).jar $(EXECUTABLE)
