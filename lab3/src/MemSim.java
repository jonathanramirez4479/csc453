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
 * TLB, Page Table, and Backing Store.  The simulator accepts a list of
 * byte addresses and reports the value at that byte address, the frame number
 * where that address is located, and the entire frame data.  Lastly,
 * the simulator reports page fault statistics.
 */

public class MemSim {

    private static final int BLOCK_SIZE = 256;

    private HashMap<Integer, TLB_Process> TLB = new HashMap<>();
    private HashMap<Integer, PageTable> pageTable = new HashMap<>();

    
    private byte frameSize = (byte) 256;
    
    private byte physicalMem = (byte) 256;

    /**
     * Driver function for virtual memory simulator
     *
     * @param args <reference-sequence-file.txt> <FRAMES> <PRA>
     */
    public static void main(String[] args) throws IOException {
        // mod to get offset
        // divide to get page number
        int frames = 256;
        String algorithm = "FIFO";



        File file = new File(args[0]);
        ArrayList<Integer> addresses =  readAddresses(file);
        String filePath = "./src/BACKING_STORE.bin";

        for(int address : addresses) {
            printData(address, filePath);
        }
    }

    /**
     * Prints the data in the frame of the physical memory, formatted per the
     * assignment requirement
     *
     * @param address The byte address to reference
     * @param filePath The string path of the backing store (always "./src/BACKING_STORE.bin")
     */
    private static void printData(int address, String filePath) {

        byte valueAtAddress = 0;
        byte[] frameData = new byte[BLOCK_SIZE];
        try (RandomAccessFile raf = new RandomAccessFile(new File(filePath), "r")) {
            raf.seek(address);
            valueAtAddress = raf.readByte();

            System.out.println("value at byte address: " + address + " = " + valueAtAddress);

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