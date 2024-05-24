package src;


public class PhysicalMemory {
    private byte[][] memory;

    public PhysicalMemory(int numOfFrames) {
        this.memory = new byte[numOfFrames][256];
    }

    public byte[] getFrameData(int index) {
        return this.memory[index];
    }

    public int addFrame(byte[] data, int index) {
        this.memory[index] = data;
        return index;
    }

    public void printFrameData(int frameIndex) {
        for(byte b : getFrameData(frameIndex)) {
            String hexString = String.format("%02X", b);
            System.out.print(hexString);
        }
        System.out.println();
    }

    public void printMemory() {
        for (int i = 0; i < 10; i++) {
            printFrameData(i);
        }
    }
}
