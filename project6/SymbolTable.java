
import java.util.*;
import java.io.*;

public class SymbolTable {

    private Map<String, Integer > mapTable;

    public SymbolTable () {
        this.mapTable = new HashMap<>();
    }

    public void addEntry(String symbol, int address) {
        this.mapTable.put(symbol, address);
    }

    public boolean contains(String symbol) {
        return this.mapTable.containsKey(symbol);
    }

    public int getAddress(String symbol) {
        return this.mapTable.get(symbol);
    }

}