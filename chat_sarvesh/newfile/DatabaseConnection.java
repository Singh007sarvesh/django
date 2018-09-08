import java.sql.*;
public class DatabaseConnection
{
	Statement statement;
	Connection connection;
	DatabaseConnection()throws Exception
  {
  	connection=DriverManager.getConnection("jdbc:mysql://localhost:3306/test","root","");
    statement=connection.createStatement();
  }
	public void insertIntoDatabase(Employee emp)
  { 
    try
    {     
      String sql= ("insert into emp_records values(\""+emp.firstName+"\",\""+emp.lastName+"\",\" " +emp.dob+"\",\""+emp.aadharId+
	      		"\",\""+emp.gender+"\",\""+emp.email+"\",\""+emp.userName+"\",\""+emp.password+"\");");
	      	statement.executeUpdate(sql);
    }
    catch(Exception e)
    { 
	      System.out.println(e);
    }  
  }
  public void closeConnection() 
  {
  	try
  	{
  			connection.close();
  	}
  	catch(Exception ex)
  	{
  			System.out.println(ex);
  	}
  }  
}