import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        String line = args[0];
        //line += ".asm";
        //if(line.length() != 1) throw new IllegalArgumentException("Not a valid file");

        File file = new File(line);
        try {
            hackAss assi = new hackAss(file);
            assi.assemble();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static class hackAss {
        private SymbolTable symbolTable;
        private File file;

        public hackAss(File file) throws IOException {
            this.symbolTable = new SymbolTable();
            this.file = file;
        }

        public void assemble() throws IOException {
            Parser parser = new Parser(this.file);
            initialization(this.symbolTable);
            firstPass(this.symbolTable, parser);
            secondPass(this.symbolTable, parser, this.file);
        }

        public void initialization(SymbolTable symbolTable) {
            //System.out.println("Start Initializing");
            for (int i = 0; i < 16; i++) {
                String symbol = "R" + i;
                symbolTable.addEntry(symbol, i);
            }
            symbolTable.addEntry("SCREEN", 16384);
            symbolTable.addEntry("KBD", 24576);
            symbolTable.addEntry("SP", 0);
            symbolTable.addEntry("LCL", 1);
            symbolTable.addEntry("ARG", 2);
            symbolTable.addEntry("THIS", 3);
            symbolTable.addEntry("THAT", 4);

            //System.out.println("End Initializing");
        }

        public void firstPass(SymbolTable symbolTable, Parser parser) throws IOException {
            int addressCount = 0;
            //System.out.println("Start First Pass");
            while (parser.hasMoreLines()) {
                parser.advance();
                if (parser.getInstType() != InstructionType.L_INSTRUCTION)
                    addressCount++;
                else
                    symbolTable.addEntry(parser.symbol(), addressCount);
            }
            //System.out.println("End First Pass");
        }

        public void secondPass(SymbolTable symbolTable, Parser parser, File file) throws IOException {
            //System.out.println("Start Second Pass");
            parser = new Parser(file);
            File output = outputFile(file);
            BufferedWriter writer = new BufferedWriter(new FileWriter(output));
            int addressCount = 16;
            while (parser.hasMoreLines()) {
                parser.advance();
                //System.out.println(parser.getInstruction());
                if (parser.getInstType() == InstructionType.A_INSTRUCTION) {
                    int masked;
                    if (!symbolTable.contains(parser.symbol())) {
                        try {
                            masked = Integer.parseInt(parser.symbol()) & 0xFFFF;
                        } catch (NumberFormatException e) {
                            symbolTable.addEntry(parser.symbol(), addressCount);
                            //System.out.println(parser.symbol() + " " + addressCount);
                            masked = addressCount & 0xFFFF;
                            addressCount++;
                        }
                    }
                    //System.out.println(parser.symbol());
                    else
                        masked = symbolTable.getAddress(parser.symbol()) & 0xFFFF;

//                if(parser.symbol() != (int)(parser.symbol()))
//                     masked = symbolTable.getAddress(parser.symbol()) & 0xFFFF;
//                else
//                    masked = Integer.parseInt(parser.symbol()) & 0xFFFF;
                    String binary = Integer.toBinaryString(masked);
                    writer.write(String.format("%16s", binary).replace(' ', '0'));
                    //System.out.println(String.format("%16s", binary).replace(' ', '0'));
                    writer.newLine();
                } else if (parser.getInstType() == InstructionType.C_INSTRUCTION) {
                    String line = "111";
                    line += Code.comp(parser.comp());
                    line += Code.dest(parser.dest());
                    line += Code.jump(parser.jump());
                    writer.write(line);
                    //System.out.println(line);
                    writer.newLine();
                }
            }
            writer.close();
            //System.out.println("End Second Pass");
        }

        public File outputFile(File input) {
            String name = input.getName();
            name = name.substring(0, name.length() - 3);
            name += "hack";
            return new File(input.getParent(), name);
        }
    }
}