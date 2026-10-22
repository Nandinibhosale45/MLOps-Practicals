
import java.util.*;

class Student
{
    int id;
    String name;
     
    void set()
    {
      Scanner sc =new Scanner(System.in);
      System.out.println("enter your rollno:");
      id=sc.nextInt();
      sc.nextLine();
      System.out.println("enter your name:");
      name=sc.nextLine();

    }
    void get()
    {
        System.out.println("std id :"+id);
        System.out.println("std name:"+name);
    }
    public static void main(String[] args) {
        Student s= new Student();
        s.set();
        s.get();
    }

}