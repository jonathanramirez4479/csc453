package src;
public class PageTable
{
    private byte pageSize = (byte) 256;
    public int validBit = 0;
    public int pageNumber;
    
public void setPage(int pageNumber)
{

}
public void getPage(int pageNumber)
{
    // perform lookup in pageTable
}
public void loadPage(){
    // load from backing store
}

}
