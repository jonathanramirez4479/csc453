package src;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Scanner;


public class MemSim {

    private HashMap<Integer, TLB_Process> TLB = new HashMap<>();
    private HashMap<Integer, PageTable> pageTable = new HashMap<>();
    
    private byte frameSize = (byte) 256;
    
    private byte physicalMem = (byte) 256;
    public static void main(String[] args) throws FileNotFoundException
    {
        // mod to get offset
        // divide to get page number
        //
        File file = new File(args[0]);
        ReadFile(file);
    }
    
    private static void ReadFile(File file) throws FileNotFoundException
    {
        Scanner fileRead = new Scanner(file);
        while(fileRead.hasNext())
        {
            int i = fileRead.nextInt();
            int pageNum = i / 256;
            int pageOffset = i % 256;
            System.out.println(i);
            System.out.println(pageNum);
            System.out.println(pageOffset);
        }
        fileRead.close();
    }
}