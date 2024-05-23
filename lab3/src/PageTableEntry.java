package src;

public class PageTableEntry {
    private int frameNumber;
    private int validBit;

    public PageTableEntry(int frameNumber, int validBit) {
        this.frameNumber = frameNumber;
        this.validBit = validBit;
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
}
