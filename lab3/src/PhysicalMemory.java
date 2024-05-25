package src;
import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;

public class PhysicalMemory {
    private byte[][] memory;
    private String PRA;
    public Queue<Integer> frameQueue;
    public int numOfFrames;
    private TLB tlb;
    private PageTable pageTable;
    private Map<Integer, Integer> accessTime;

    public PhysicalMemory(int numOfFrames, String _PRA, TLB _tlb, PageTable _pageTable) {
        this.memory = new byte[numOfFrames][256];
        this.PRA = _PRA;
        this.numOfFrames = numOfFrames;
        this.frameQueue = new ArrayDeque<>();
        this.tlb = _tlb;
        this.pageTable = _pageTable;
        this.accessTime = new HashMap<>();
    }

    public byte[] getFrameData(int index) {
        return this.memory[index];
    }

    public int addFrame(byte[] data, int index) {

        if (frameQueue.size() >= numOfFrames) {
            int evictedFrame = evictFrame();
            PageTableEntry entry = pageTable.getPageTableEntryByFrame(evictedFrame);
            entry.setValidBit(0);
            tlb.removeTlbEntry(evictedFrame);
            this.memory[evictedFrame] = data;
            frameQueue.add(evictedFrame);
            accessTime.put(evictedFrame, 0); // Reset access time for evicted frame
            return evictedFrame;
        }
        else {
            this.memory[index] = data;
            frameQueue.add(index);
            accessTime.put(index, 0); // Reset access time for evicted frame
            return index;
        }
    }

    public int evictFrame() {
        int evictedFrame = 0;
        switch (PRA) {
            case "LRU":
                int minAccessTime = Integer.MAX_VALUE;
                for (int frame : frameQueue) {
                    if (accessTime.get(frame) < minAccessTime) {
                        minAccessTime = accessTime.get(frame);
                        evictedFrame = frame;
                    }
                }
                frameQueue.remove(evictedFrame);
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