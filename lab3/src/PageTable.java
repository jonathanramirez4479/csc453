package src;

public class PageTable {

    private static final int PAGE_TABLE_LENGTH = (int) Math.pow(2, 8);
    public Page[] table;

    public PageTable() {
        this.table = new Page[PAGE_TABLE_LENGTH];
    }

    public void setPage(Page _page, int pageOffset) {
        table[pageOffset] = _page;
    }

    public void createNewPage(Integer pageOffset, Integer pageNumber, Integer frameNumber, Integer tlbAccessed) {
        table[pageOffset] = new Page(pageNumber, frameNumber, tlbAccessed);
    }

    public Page getPage(int pageNumber) {
        if (pageNumber >= 0 && pageNumber < PAGE_TABLE_LENGTH) {
            return table[pageNumber];
        } else {
            return null;
        }
    }
}
