package src;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

/**
 * This class represents a virtual memory simulator that contains a
 * TLB, TlbEntry Table, and Backing Store.  The simulator accepts a list of
 * byte addresses and reports the value at that byte address, the frame number
 * where that address is located, and the entire frame data.  Lastly,
 * the simulator reports page fault statistics.
 */

public class memSim {

    private static final int BLOCK_SIZE = 256;
    private static final int PAGE_SIZE = 256;
    private static int tlbNumHits = 0;
    private static int tlbNumMisses = 0;
    private static int pageFaults = 0;
    private static TLB tlb;
    private static PhysicalMemory memory;
    private static HashMap<Integer, Integer> pageInstructionCounts; // page num -> count

    /**
     * Driver function for virtual memory simulator
     *
     * @param args <reference-sequence-file.txt> <FRAMES> <PRA>
     */
    public static void main(String[] args) throws IOException {
        // mod to get offset
        // divide to get page number
        int numOfFrames = 256;
        String PRA = "FIFO";
        if (args.length > 1)
        {
            numOfFrames = Integer.parseInt(args[1]);
            if (args.length > 2)
            {
                PRA = args[2];
            }
        }

        tlb = new TLB();
        PageTable pageTable = new PageTable();
        memory = new PhysicalMemory(numOfFrames, PRA, tlb, pageTable);

        // read byte address accesses and store them in a list
        File file = new File(args[0]);
        ArrayList<Integer> addresses = readAddresses(file);

        pageInstructionCounts = getPageInstructionCounts(addresses);

        String filePath = "./src/BACKING_STORE.bin";

        int i = 0;
        for (int address : addresses) {
            int pageNumber = address / PAGE_SIZE;

            //entering tlb
            if (pageNumber <= PAGE_SIZE) {
                if (tlb.containsPageNumber(pageNumber)) {
                    tlbNumHits+=1;
                    TlbEntry tlbEntry = tlb.getTlbEntry(pageNumber);
                    if (tlbEntry != null) {
                        tlb.updateAllAccesses(tlbEntry);
                    }
                    PageTableEntry pageTableEntry = pageTable.getPageTableEntry(pageNumber);
                    if (pageTableEntry != null) { // LRU
                        pageTableEntry.resetAccessTime();
                        memory.incrementOtherAccessTimes(pageTableEntry.getFrameNumber());
                    }
                    byte[] blockData = memory.getFrameData(tlbEntry.getFrameNumber());
                    byte valueAtAddress = blockData[tlbEntry.getFrameNumber()];

                    decrementPageInstructionCount(pageNumber);
                    memory.updateFrameInstructionCount(tlbEntry.getFrameNumber(),
                            pageInstructionCounts.get(pageNumber));


                    System.out.printf("%d, %d, %d,\n", address,valueAtAddress, tlbEntry.getFrameNumber());
                    continue;
                }
                tlbNumMisses+=1;
                //entering page table -> tlb
                if (pageTable.containsPageNumber(pageNumber)) {
                    //page table hit
                    PageTableEntry pageTableEntry = pageTable.getPageTableEntry(pageNumber);
                    if (pageTableEntry.getValidBit() == 1)
                    {
                        tlb.addTlbEntry(new TlbEntry(pageNumber, pageTableEntry.getFrameNumber()));

                        pageTableEntry.resetAccessTime();// LRU
                        memory.incrementOtherAccessTimes(pageTableEntry.getFrameNumber());

                        byte[] blockData = memory.getFrameData(pageTableEntry.getFrameNumber());
                        byte valueAtAddress = blockData[pageTableEntry.getFrameNumber()];

                        decrementPageInstructionCount(pageNumber);
                        memory.updateFrameInstructionCount(pageTableEntry.getFrameNumber(),
                            pageInstructionCounts.get(pageNumber));

                        System.out.printf("%d, %d, %d,\n", address,valueAtAddress, pageTableEntry.getFrameNumber());
                        continue;
                    }
                }

                pageFaults+=1;
                // hard miss
                //entering backing store -> pagetable -> tlb
                byte[] blockData = getBlockData(address, filePath);
                int frameIndex = memory.addFrame(blockData, i);

                decrementPageInstructionCount(pageNumber);
                memory.updateFrameInstructionCount(frameIndex, pageInstructionCounts.get(pageNumber));

                i++;
                pageTable.populateEntry(pageNumber, new PageTableEntry(frameIndex, 1));
                tlb.addTlbEntry(new TlbEntry(pageNumber, frameIndex));
                byte valueAtAddress = blockData[address % PAGE_SIZE];
                System.out.printf("%d, %d, %d,\n", address, (int) valueAtAddress, frameIndex);
                memory.printFrameData(frameIndex);
            } else {
                System.out.println("Virtual address is out of bounds");
            }
//            memory.printFrames();
        }
//        System.out.println("simulation finished, dumping TLB");
//        tlb.printTLB();
        float tlbHitRate = (float)tlbNumHits / addresses.size();
        float pageFaultRate = (float) pageFaults / addresses.size();
        System.out.printf("Number of Translated Addresses %d" +
                "\nPage Faults = %d\n" +
                "Page Fault Rate = %.3f\n" +
                "TLB Hits = %d\n" +
                "TLB Misses = %d\n" +
                "TLB Hit Rate = %.3f\n", addresses.size(), pageFaults, pageFaultRate, tlbNumHits, tlbNumMisses,
                tlbHitRate);

    }

    private static void printPageInstructionCounts() {
        System.out.println(pageInstructionCounts);
    }

    private static void decrementPageInstructionCount(Integer pageNumber) {
        Integer currentCount = pageInstructionCounts.get(pageNumber);
        pageInstructionCounts.put(pageNumber, currentCount - 1);
    }

    private static HashMap<Integer, Integer> getPageInstructionCounts(ArrayList<Integer> addresses) {
        HashMap<Integer, Integer> pageInstructionCounts = new HashMap<>();
        for (Integer address : addresses) {
            Integer pageNumber = address / PAGE_SIZE;
            if (pageInstructionCounts.containsKey(pageNumber)) {
                int currentValue = pageInstructionCounts.get(pageNumber);
                pageInstructionCounts.put(pageNumber, currentValue + 1);
            } else {
                pageInstructionCounts.put(pageNumber, 1);
            }
        }

        return pageInstructionCounts;
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
     * @param address  The byte address to reference
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

        for (byte b : frameData) {
            String hexString = String.format("%02X", b);
            System.out.print(hexString);
        }
        System.out.println();

    }

    private static ArrayList<Integer> readAddresses(File file) throws FileNotFoundException {
        ArrayList<Integer> addresses = new ArrayList<>();
        Scanner fileRead = new Scanner(file);
        while (fileRead.hasNext()) {
            Integer i = fileRead.nextInt();
            addresses.add(i);
        }
        fileRead.close();

        return addresses;
    }
}