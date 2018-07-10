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
    void getCommand()
    {
        while(1)
        {
            System.out.println("Enter one of the following commands:);
            System.out.println("Input\nDisplay\nfilter\nexit");
            cmd = reader.nextLine();
            if (cmd.toLowerCase().equals("input"))
            {
            } else if (cmd.toLowerCase().equals("display")) {

            } else if (cmd.toLowerCase().equals("filter")) {

            } else if (cmd.toLowerCase().equals("exit")) {
                System.exit(0);
            }
        }
    }
    public static void main(String[] args)
    {
        Assignment1 obj;
        obj.reader = new Scanner(System.in);
        System.out.println("starting application");
        obj.getCommand()
    }
