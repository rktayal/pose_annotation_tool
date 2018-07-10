import java.util.Scanner;

/***
 *
 * Class's Author Name  :   Rachit Tayal
 * Last Modified        :   July 10, 2018
 *
 ***/
public class Assignment1
{
    Scanner reader;
    int[] data;
    Assignment1()
    {
        reader = new Scanner(System.in);
    }

    int[] removeNegatives(int[] arr)
    {
        int count = arr.length;
        for (int i = 0; i < arr.length; i++)
        {
            if (arr[i] < 0)
                count--;
        }
        int[] new_arr = new int[count];
        for (int i = 0, j=0; i < arr.length; i++)
        {
            if (arr[i] < 0) continue;
            new_arr[j++] = arr[i];
        }
        displayContents(new_arr);
        return new_arr;
        
    }

    void displayContents(int[] arr)
    {
        for (int i =0; i < arr.length; i++)
        {
            System.out.printf("Array element %d: %d\n", i+1, arr[i]);
        }
    }

    void getInput()
    {
        int size;
        System.out.print("Enter array size\t:");
        size = reader.nextInt();
        data = new int[size];
        for (int i=0; i < size; i++)
        {
            data[i] = reader.nextInt();
        }
        reader.nextLine();
        displayContents(data);
    }

    void getCommand()
    {
        String cmd;
        while(true)
        {
            System.out.println("Enter one of the following commands:");
            System.out.println("Input\nDisplay\nfilter\nexit");
            System.out.print("Enter Cmd\t:");
            cmd = reader.nextLine();
            if (cmd.toLowerCase().equals("input"))
            {
                getInput();
            }
            else if (cmd.toLowerCase().equals("display"))
            {
                displayContents(data);
            }
            else if (cmd.toLowerCase().equals("filter"))
            {
                int[] arr;
                arr = removeNegatives(data);
            }
            else if (cmd.toLowerCase().equals("exit"))
            {
                System.exit(0);
            }
        }
    }

    public static void main(String[] args)
    {
        Assignment1 obj = new Assignment1();
        System.out.println("starting application");
        obj.getCommand();
    }
}
