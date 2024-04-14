public class TestIndexOutOfBounds {
    public static void main(String[] args) {
        int[] array = new int[5];
        int index = 5;  // Invalid index, array length is 5 (indices 0-4 are valid)
        array[index] = 100;  // This line will throw ArrayIndexOutOfBoundsException
        System.out.println(array[index]);
    }
}