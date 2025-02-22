package src;
public class PageTable {

    private PageTableEntry[] pageTable;

    public PageTable() {
        int pageTableSize = 256;
        pageTable = new PageTableEntry[pageTableSize];
    }

    public boolean containsPageNumber(int pageNumberIndex) {
        if (this.pageTable[pageNumberIndex] != null) {
            return true;
        }
        return false;
    }

    public int getPageNumberByPageTableEntry(PageTableEntry pageTableEntry) {
        int pageNumber = 0;
        for (int i = 0; i < pageTable.length; i++) {
            PageTableEntry p = pageTable[i];
            if (p == null) {
                continue;
            }
            if (p.equals(pageTableEntry)){
                pageNumber = i;
                break;
            }
        }
        return pageNumber;
    }

    public void populateEntry(int pageNumberIndex, PageTableEntry entry) {
        this.pageTable[pageNumberIndex] = entry;
    }

    public PageTableEntry getPageTableEntry(int pageNumberIndex) {
        return this.pageTable[pageNumberIndex];
    }
    public PageTableEntry getPageTableEntryByFrame(int pageNumberFrame) {
        for (PageTableEntry entry : pageTable) {
            if (entry != null && entry.getFrameNumber() == pageNumberFrame) {
                return entry;
            }
        }
        return null; // Return null if no matching entry is found
    }
}
