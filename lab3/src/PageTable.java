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
