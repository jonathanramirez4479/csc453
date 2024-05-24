package src;


import java.util.ArrayDeque;
import java.util.PriorityQueue;
import java.util.Queue;

public class PhysicalMemory {
    private byte[][] memory;
    private String PRA;
    private Queue<Integer> frameQueue;
    private int numOfFrames;

    public PhysicalMemory(int numOfFrames, String _PRA) {
        this.memory = new byte[numOfFrames][256];
        this.PRA = _PRA;
        this.numOfFrames = numOfFrames;
        this.frameQueue = new ArrayDeque<>();
    }

    public byte[] getFrameData(int index) {
        return this.memory[index];
    }

    public int addFrame(byte[] data, int index) {
        if (frameQueue.size() >= numOfFrames) {
            int evictedFrame = evictFrame();
            this.memory[evictedFrame] = data;
            frameQueue.add(evictedFrame);
            return evictedFrame;
        } else {
            this.memory[index] = data;
            frameQueue.add(index);
            return index;
        }
    }

    private int evictFrame() {
        int evictedFrame = 0;
        switch (PRA) {
            case "LRU":
                break;
            case "OPT":
                break;
            default:
                evictedFrame = frameQueue.poll();  // FIFO
                break;
        }
        return evictedFrame;
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
