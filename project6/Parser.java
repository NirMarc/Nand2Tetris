
import java.io.*;
import java.util.*;

public class Parser {
    private File file;
    private BufferedReader reader;
    private String instrcution;
    private InstructionType instType;

    public Parser (File source) throws FileNotFoundException, IOException {
        this.file = source;
        this.reader = new BufferedReader(new FileReader(source));
        this.instrcution = "";
        this.instType = null;
    }

    public boolean hasMoreLines () throws IOException {
        this.reader.mark(1);
        if (this.reader.read() == -1) return false;
        this.reader.reset();
        return true;
    }

    public void advance() throws IOException {
        if(this.hasMoreLines()) {
            this.instrcution = reader.readLine();
            this.instrcution = this.instrcution.trim();
            //System.out.println(this.instrcution);
             while(!checkValidLine(this.instrcution)) {
                 this.instrcution = reader.readLine();
                 this.instrcution = this.instrcution.trim();
                 //System.out.println("inWhile");
             }
            this.instType = InstructionType.getInstructionType(this.instrcution);
            //System.out.println(this.instrcution);
        }
        else System.out.println("No more lines");
    }

    public boolean checkValidLine(String line) throws IOException {
        //boolean checkValid = true;
        if (line.isEmpty()) return false;
        switch(line.charAt(0)) {
            case '@':
                return true;
            case '(':
                return true;
            case 'A':
                return true;
            case 'D':
                return true;
            case 'M':
                return true;
            case '0':
                return true;
//            case ' ':
//                return true;
        }
        return false;
    }

    public InstructionType instructionType() {
        return instType.getInstructionType(this.instrcution);
    }

    public String symbol() {
        switch(this.instType) {
            case A_INSTRUCTION:
                return this.instrcution.substring(1);
            case L_INSTRUCTION:
                return this.instrcution.substring(1, this.instrcution.length() - 1);
            default:
                return this.instrcution;
        }
    }

    public String dest() {
        //System.out.println(this.instrcution);
        if (this.instrcution.indexOf('=') == - 1)
            return null;
        return this.instrcution.substring(0, this.instrcution.indexOf((int)('=')));
    }

    public String comp() {
        //System.out.println(this.instrcution);
        if (this.instrcution.indexOf('=') == - 1)
            return this.instrcution.substring(0, 1);
        else if (this.instrcution.indexOf(';') == - 1)
            return this.instrcution.substring(this.instrcution.indexOf((int)('=')) + 1);
        else
            return this.instrcution.substring(this.instrcution.indexOf((int)('=') + 1), this.instrcution.indexOf(';') - 1);
    }

    public String jump() {
        if (this.instrcution.indexOf(';') == - 1)
            return null;
        else {
            return this.instrcution.substring(this.instrcution.indexOf(';') + 1);
        }
    }

    public InstructionType getInstType() {
        return instType;
    }

    public String getInstruction() {
        return this.instrcution;
    }


}