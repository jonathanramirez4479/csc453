package src;


public class PhysicalMemory {
    private byte[][] memory;

    public PhysicalMemory(int numOfFrames) {
        this.memory = new byte[10][256];
    }

    public byte[] getFrameData(int index) {
        return this.memory[index];
    }

    public void addFrame(byte[] data, int index) {
        this.memory[index] = data;
    }

    public int getSegments() {
        return this.memory.length;
    }
}
