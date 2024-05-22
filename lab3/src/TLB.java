package src;
import java.util.ArrayList;

public class TLB {
    private ArrayList<Page> TlbList;
    private final int TLB_MAX_SIZE = 16;

    public TLB() {
        this.TlbList = new ArrayList<>(TLB_MAX_SIZE);
    }

    /**
     * This function checks if a page is in the TLB
     *
     * @param pageNumber The page number we want to access
     * @return True if found in the TLB, False otherwise
     */

    public boolean containsPageNumber(Integer pageNumber) {
       // iterate through the pages in the TLB
       for (Page currentPage : TlbList) {
           if (currentPage.getPageNumber() == pageNumber) {
                return true;
           }
       }
       return false;
    }

    public void addPageToTLB(Page page) {
        this.TlbList.add(page);
    }

    /**
     * This function updates the accesses of each slot in the TLB with the exception of the 'page' param
     *
     * @param page  The page that should not get updated by this function
     */

    public void updateAllAccesses(Page page) {
        for (Page current : TlbList) {
            if (current != page) {
                current.setTlbAccessed(current.getTlbAccessed() + 1);
            }
        }
    }

    public void printTLB() {
        for (Page page : this.TlbList) {
            System.out.println("page number: " + page.getPageNumber() + ", access: " +
                    page.getTlbAccessed() + ", frame number: " + page.getFrameNumber());
        }
    }
}
