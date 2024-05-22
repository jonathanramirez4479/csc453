package src;

public class Page {
    private Integer pageNumber;
    private Integer frameNumber;
    private Integer tlbAccessed;

    public Page(Integer pageNumber, Integer frameNumber, Integer tlbAccessed) {
        this.pageNumber = pageNumber;
        this.frameNumber = frameNumber;
        this.tlbAccessed = tlbAccessed;
    }

    public Integer getPageNumber() {
        return this.pageNumber;
    }

    public Integer getFrameNumber() {
        return this.frameNumber;
    }

    public Integer getTlbAccessed() {
        return this.tlbAccessed;
    }

    public void setPageNumber(Integer pageNumber) {
        this.pageNumber = pageNumber;
    }

    public void setFrameNumber(Integer frameNumber) {
        this.frameNumber = frameNumber;
    }

    public void setTlbAccessed(Integer tlbAccessed) {
        this.tlbAccessed = tlbAccessed;
    }
}
