package src;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.lang.Math;

/**
 * This class represents a virtual memory simulator that contains a
 * TLB, Page Table, and Backing Store.  The simulator accepts a list of
 * byte addresses and reports the value at that byte address, the frame number
 * where that address is located, and the entire frame data.  Lastly,
 * the simulator reports page fault statistics.
 */

public class MemSim {

    private static final int BLOCK_SIZE = 256;
    private static final int FRAME_SIZE = 256;
   // private static PageTable pageTable = new PageTable();

    // page table hashmap with key value <Page # and valid bit>
    private static TLB tlb = new TLB();
    private static PhysicalMemory memory;
    /**
     * Driver function for virtual memory simulator
     *
     * @param args <reference-sequence-file.txt> <FRAMES> <PRA>
     */
    public static void main(String[] args) throws IOException
    {

        HashMap<Integer, Integer> pageTable = new HashMap();
        // mod to get offset
        // divide to get page number
        int numOfFrames = 10;

        memory = new PhysicalMemory(numOfFrames); // init memory structure with number of frames passed in

        // read byte address accesses and store them in a list
        try
        {
            File file = new File(args[0]);
            ArrayList<Integer> addresses =  readAddresses(file);
            // check TLB

            for (int address : addresses) {
                int pageNum = address / BLOCK_SIZE;
                int page_offset = address % BLOCK_SIZE;
                pageTable.put(pageNum, 0);
                if (!tlb.containsPageNumber(pageNum))
                {
                    if (pageTable.containsKey(pageNum))
                    {

                    }
                }
            }
            // go to page table (on miss)
            // go to disk (backing store on miss)

            String filePath = "./src/BACKING_STORE.bin";

            int i = 0;
            for(int address : addresses)
            {
                byte[] currentFrame = getBlockData(address, filePath);
                memory.addFrame(currentFrame, i);
                i++;
            }
        }
        catch(Exception e)
        {

        }

//            printData(address, filePath);
//            Integer pageNumber = address / PAGE_SIZE;
//            Page page = new Page(pageNumber, null, null);
//
//            page.setTlbAccessed(1);
//            tlb.updateAllAccesses(page);
//
//            if (!tlb.containsPageNumber(pageNumber)) {
//                tlb.addPageToTLB(page);
//            }
        }

    private static byte[] getBlockData(int address, String filePath) throws RuntimeException {
        byte[] blockData = new byte[BLOCK_SIZE];
        try (RandomAccessFile raf = new RandomAccessFile(new File(filePath), "r")) {
            int frameStartPos = (address / BLOCK_SIZE) * BLOCK_SIZE;
            raf.seek(frameStartPos);
            raf.read(blockData);

            return blockData.clone();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


    /**
     * Prints the data in the frame of the physical memory, formatted per the
     * assignment requirement
     *
     * @param address The byte address to reference
     * @param filePath The string path of the backing store (always "./src/BACKING_STORE.bin")
     */
    public static void printData(int address, String filePath) {

        byte valueAtAddress = 0;
        byte[] frameData = new byte[BLOCK_SIZE];
        try (RandomAccessFile raf = new RandomAccessFile(new File(filePath), "r")) {
            raf.seek(address);
            valueAtAddress = raf.readByte();


            int frameStartPos = (address / BLOCK_SIZE) * BLOCK_SIZE;

            raf.seek(frameStartPos);
            raf.read(frameData);
        } catch (IOException e) {
            System.out.println("Error while reading BACKING_STORE.bin");
        }

        System.out.println(address + ", " + valueAtAddress + ", " + 0);

        for(byte b : frameData) {
            String hexString = String.format("%02X", b);
            System.out.print(hexString);
        }
        System.out.println();
    }
    
    private static ArrayList<Integer> readAddresses(File file) throws FileNotFoundException {
        ArrayList<Integer> addresses = new ArrayList<>();
        Scanner fileRead = new Scanner(file);
        while(fileRead.hasNext()) {
            Integer i = fileRead.nextInt();
            addresses.add(i);
        }
        fileRead.close();

        return addresses;
    }
}