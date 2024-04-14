import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class JavaCodeGenerator {

    private static final String DESKTOP_PATH = System.getProperty("user.home") + File.separator + "Desktop";
    private static final String BASE_DIRECTORY = DESKTOP_PATH + File.separator + "Training Prompts";
    private static final String ERROR_DIRECTORY = BASE_DIRECTORY + File.separator + "error";
    private static final String NO_ERROR_DIRECTORY = BASE_DIRECTORY + File.separator + "no_error";

    private static final Random random = new Random();

    public static void main(String[] args) {
        // Create directories if not exist
        createDirectories();

        // Generate Java code snippets
        generateCodeSnippets(100000); // Change the number as desired
    }

    private static void createDirectories() {
        File baseDir = new File(BASE_DIRECTORY);
        if (!baseDir.exists()) {
            baseDir.mkdirs();
        }

        File errorDir = new File(ERROR_DIRECTORY);
        if (!errorDir.exists()) {
            errorDir.mkdirs();
        }

        File noErrorDir = new File(NO_ERROR_DIRECTORY);
        if (!noErrorDir.exists()) {
            noErrorDir.mkdirs();
        }
    }

    private static void generateCodeSnippets(int numSnippets) {
        for (int i = 1; i <= numSnippets; i++) {
            String code = generateCodeSnippet();
            String fileName = i + ".txt";
            String directory = code.contains("ERROR") ? ERROR_DIRECTORY : NO_ERROR_DIRECTORY;
            writeFile(directory + File.separator + fileName, code);
        }
    }

    private static String generateCodeSnippet() {
        StringBuilder code = new StringBuilder();

        // Generate random code snippet
        int arraySize = random.nextInt(10) + 1; // Random array size from 1 to 10
        int index = random.nextInt(2 * arraySize) - arraySize; // Random index within -arraySize to arraySize range

        if (index < 0 || index >= arraySize) {
            code.append("public class ErrorSnippet").append(" {\n");
            code.append("    public static void main(String[] args) {\n");
            code.append("        int[] array = new int[").append(arraySize).append("];\n");
            code.append("        int index = ").append(index).append(";\n");
            code.append("        System.out.println(array[index]); // ERROR: Index out of bounds\n");
            code.append("    }\n");
            code.append("}\n");
        } else {
            code.append("public class NoErrorSnippet").append(" {\n");
            code.append("    public static void main(String[] args) {\n");
            code.append("        int[] array = new int[").append(arraySize).append("];\n");
            code.append("        int index = ").append(index).append(";\n");
            code.append("        array[index] = ").append(index).append(";\n");
            code.append("        System.out.println(array[index]);\n");
            code.append("    }\n");
            code.append("}\n");
        }

        return code.toString();
    }

    private static void writeFile(String filePath, String content) {
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
