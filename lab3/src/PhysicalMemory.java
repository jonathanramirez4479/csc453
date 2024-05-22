package src;

import java.util.ArrayList;

public class PhysicalMemory {
    private ArrayList<Page> memory;

    public PhysicalMemory(int numOfFrames) {
        this.memory = new ArrayList<>(numOfFrames);
    }

    public Page getFrame(int index) {
        return this.memory.get(index);
    }


}
