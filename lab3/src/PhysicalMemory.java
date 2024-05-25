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

    public PhysicalMemory(int numOfFrames, String _PRA, TLB _tlb, PageTable _pageTable) {
        this.memory = new byte[numOfFrames][256];
        this.PRA = _PRA;
        this.numOfFrames = numOfFrames;
        this.frameQueue = new ArrayDeque<>();
        this.tlb = _tlb;
        this.pageTable = _pageTable;
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
            entry.resetAccessTime(); // LRU
            incrementOtherAccessTimes(entry.getFrameNumber()); // LRU
            return evictedFrame;
        }
        else {
            this.memory[index] = data;
            frameQueue.add(index);
            incrementOtherAccessTimes(index);
            return index;
        }
    }

    public int evictFrame() {
        int evictedFrame = 0;
        int leastRecentlyUsed = 0;
        switch (PRA) {
            case "LRU":
                for (int frame : frameQueue) {
                    PageTableEntry entry = pageTable.getPageTableEntryByFrame(frame);
                    if (entry.getAccessTime() > leastRecentlyUsed) {
                        leastRecentlyUsed = entry.getAccessTime();
                        evictedFrame = entry.getFrameNumber();
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

    public void incrementOtherAccessTimes(int frameNumber) {
        for (int frame : frameQueue) {
            if (!(frame == frameNumber))
            {
                PageTableEntry entry = pageTable.getPageTableEntryByFrame(frame);
                entry.incrementAccessTime();
            }

        }
    }

    public void printFrames()
    {
        for (int i = 0; i < frameQueue.size(); i++) {
            PageTableEntry entry = pageTable.getPageTableEntryByFrame(i);
            System.out.printf("Frame: %d, AccessTime: %d\n", i, entry.getAccessTime());
        }
    }
}