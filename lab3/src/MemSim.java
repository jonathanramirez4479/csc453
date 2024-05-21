package src;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


public class MemSim {

    private List<TLB_Process> TLB = new ArrayList<TLB_Process>();
    private List<PageTable> pageTable = new ArrayList<PageTable>();
    
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