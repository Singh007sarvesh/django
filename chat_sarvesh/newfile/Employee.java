class Employee
{
  String firstName; 
  String lastName;
  String dob;
  String aadharId;
  String gender;
  String email;
  String userName;
  String password;
  @Override
  public String toString() 
  {
    return firstName + " " + lastName + " "+" "+dob+" "+ aadharId +" "+gender+" "+email+" "+userName+" "+password;
  }
}
