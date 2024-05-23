package src;

import java.util.ArrayList;
import java.util.HashMap;

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
}
