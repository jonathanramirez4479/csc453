package src;

public class TlbEntry {
    private int pageNumber;
    private int frameNumber;
    private int tlbAccessed;

    public TlbEntry(int pageNumber, int frameNumber) {
        this.pageNumber = pageNumber;
        this.frameNumber = frameNumber;
    }

    public int getPageNumber() {
        return this.pageNumber;
    }

    public int getFrameNumber() {
        return this.frameNumber;
    }

    public int getTlbAccessed() {
        return this.tlbAccessed;
    }

    public void setPageNumber(int pageNumber) {
        this.pageNumber = pageNumber;
    }

    public void setFrameNumber(int frameNumber) {
        this.frameNumber = frameNumber;
    }

    public void setTlbAccessed(int tlbAccessed) {
        this.tlbAccessed = tlbAccessed;
    }
}
