import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.File;
import java.util.ArrayList;
import java.util.*;
class CsvReaderFile
{
    public List<Employee> csvReader(File csvFile) throws Exception
    {
        List <Employee> list = new ArrayList<>();
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";
        Employee employee2 = new Employee();
        br = new BufferedReader(new FileReader(csvFile));
        while ((line = br.readLine()) != null) 
        {
            String[]  sql = line.split(cvsSplitBy);
            for(int i=0;i<sql.length;i++)
            {
                if(sql[i].charAt(0)=='"')
                {
                    String str=sql[i].substring(1,sql[i].length()-1);
                    sql[i]=str;    
                }
            }
            employee2.firstName =sql[0];
            employee2.lastName = sql[1];
            employee2.dob =sql[2];
            employee2.aadharId = sql[3];
            employee2.gender =sql[4];
            employee2.email = sql[5];
            employee2.userName = sql[6];
            employee2.password = sql[7];
            list.add(employee2);
        }
        return list ;
    }
}
