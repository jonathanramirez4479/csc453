package src;
import java.util.ArrayList;

public class TLB {
    private ArrayList<TlbEntry> TlbList;
    int tlbMaxSize = 16;


    public TLB() {
        this.TlbList = new ArrayList<>(tlbMaxSize);
    }

    /**
     * This function checks if a page is in the TLB
     *
     * @param pageNumber The page number we want to access
     * @return True if found in the TLB, False otherwise
     */

    public boolean containsPageNumber(int pageNumber) {
       // iterate through the pages in the TLB
        for (TlbEntry currentTlbEntry : TlbList) {
            if (currentTlbEntry.getPageNumber() == pageNumber) {
                return true;
            }
       }
        return false;
    }

    public void addTlbEntry(TlbEntry tlbEntry) {

        if (this.TlbList.size() == tlbMaxSize) {
            TlbEntry entryPopulatedEarliest = this.TlbList.get(0);
            TlbEntry entryToRemove = null;
            for (TlbEntry entry : this.TlbList) {
                if (entry.getTlbAccessed() >= entryPopulatedEarliest.getTlbAccessed()) {
                    entryToRemove = entry;
                }
            }
            this.TlbList.remove(entryToRemove);
            tlbEntry.setTlbAccessed(1);
            this.TlbList.add(tlbEntry);
            updateAllAccesses(tlbEntry);
        }
        else {
            tlbEntry.setTlbAccessed(1);
            this.TlbList.add(tlbEntry);
            updateAllAccesses(tlbEntry);
        }
    }

    public TlbEntry getTlbEntry(int pageNumber) {
        for (TlbEntry tlbEntry : this.TlbList) {
            if (tlbEntry.getPageNumber() == pageNumber) {
                return tlbEntry;
            }
        }
        return null;
    }

    /**
     * This function updates the accesses of each slot in the TLB with the exception of the 'tlbEntry' param
     *
     * @param tlbEntry  The tlbEntry that should not get updated by this function
     */

    public void updateAllAccesses(TlbEntry tlbEntry) {
        for (TlbEntry current : TlbList) {
            if (current != tlbEntry) {
                current.setTlbAccessed(current.getTlbAccessed() + 1);
            }
        }
    }

    public void printTLB() {
        for (TlbEntry tlbEntry : this.TlbList) {
            System.out.println("tlbEntry number: " + tlbEntry.getPageNumber() + ", access: " +
                    tlbEntry.getTlbAccessed() + ", frame number: " + tlbEntry.getFrameNumber());
        }
    }
}
