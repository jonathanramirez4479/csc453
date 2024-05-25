package src;

public class PageTableEntry {
    private int frameNumber;
    private int validBit;
    private int accessTime;

    public PageTableEntry(int frameNumber, int validBit) {
        this.frameNumber = frameNumber;
        this.validBit = validBit;
        this.accessTime = 0;
    }

    public void setFrameNumber(int frameNumber) {
        this.frameNumber = frameNumber;
    }

    public void setValidBit(int validBit) {
        this.validBit = validBit;
    }

    public int getFrameNumber() {
        return this.frameNumber;
    }

    public int getValidBit() {
        return this.validBit;
    }

    public void incrementAccessTime() {
        this.accessTime++;
    }

    public void resetAccessTime()
    {
        this.accessTime = 0;
    }

    public int getAccessTime() {
        return this.accessTime;
    }
}
