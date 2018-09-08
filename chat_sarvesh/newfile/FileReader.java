import java.io.File;
import java.util.*;
public class FileReader
{
    public void sendData(File file,List<Employee> list) throws Exception
    {
        if(getFileExtension(file).equals("json"))
        {
            JsonRead json1=new JsonRead();
            list = json1.read(file);
        }
        else if(getFileExtension(file).equals("xml"))
        {
            SaxParserFactory saxParserFactory=new SaxParserFactory();
            list = saxParserFactory.readSaxParserFactory(file);
        }
        else if(getFileExtension(file).equals("csv"))
        {
            CsvReaderFile csvReader=new CsvReaderFile();
            list=csvReader.csvReader(file);
        }
        else
        {
            System.out.println("Please Read proper extension file ");
        }   
        DatabaseConnection databaseConnection=new DatabaseConnection();
        for ( Employee employee2 : list )
        {
            EmailValidate emailValidate=new EmailValidate();
            if(emailValidate.isEmailValid(employee2.email))
            {
                databaseConnection.insertIntoDatabase(employee2);
            }
            else
            {
                System.out.println("Please Enter Valid Email");
            }
        }
        databaseConnection.closeConnection();       
    }
    public static void main(String[] args)
    {
        try
        {
            String  fileName=  args[0];
            File file=new File(fileName);
            List<Employee> list=new ArrayList<>();
            FileReader fileReader=new FileReader();
            fileReader.sendData(file,list);
        }
        catch(Exception e)
        {
            System.out.println("File Not Found Pls Verify It");
        }
    }
    private static String getFileExtension(File file) 
    {
        String fileName = file.getName();
        if(fileName.lastIndexOf(".") != -1 && fileName.lastIndexOf(".") != 0)
        return fileName.substring(fileName.lastIndexOf(".")+1);
        else return "";
    }
}