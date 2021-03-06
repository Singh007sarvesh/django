import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Iterator;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.io.File;
import java.util.ArrayList;
import java.util.*;
 
class JsonRead
{
    public List<Employee> read(File file) throws Exception
    {
        List <Employee> list = new ArrayList<>();
        Object obj = new JSONParser().parse(new FileReader(file));
        JSONArray emp = (JSONArray) obj;
        Iterator<String> it = emp.iterator();
        while(it.hasNext())
        {
            Object a = (Object)it.next();
            JSONObject j = (JSONObject)a;
            JSONObject jo= (JSONObject)j.get("employee");
            Employee employee2 = new Employee();
            employee2.firstName = (String) jo.get("first_name");
            employee2.lastName = (String) jo.get("last_name");
            employee2.dob = (String) jo.get("date_of_birth");
            employee2.aadharId = (String) jo.get("aadahr_id");
            employee2.gender = (String) jo.get("gender");
            employee2.email = (String) jo.get("email");
            employee2.userName = (String) jo.get("username");
            employee2.password = (String) jo.get("password");
            list.add(employee2);
        }
        return list;
    }
}
