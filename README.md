
# **University Management System**

## **Project Overview**

The University Management System is a comprehensive web application built to streamline and manage various administrative tasks in a university environment. It enables the management of students, faculty, departments, courses, and other academic data, providing a user-friendly platform for administrators, HODs, and faculty members.  

### **Key Features**  
- **Role-based Access**: User roles include Admin, HOD, and Faculty, with varying permissions.  
- **Centers and Departments Management**: Add and manage multiple centers, each with multiple departments.  
- **Course Management**: Assign courses to departments and link them with students.  
- **Student Records**: Maintain student data, including registration numbers, attendance, fees, and internal marks.  
- **Subject and Mark Management**: Track marks by subject and semester for students.  
- **Attendance Management**: Monitor attendance with automated percentage calculation.  
- **Faculty Verification System**: Manage faculty verification requests and approval processes.  
- **Admin Dashboard**: Enhanced with custom views and filters to simplify management tasks.  

---

## **Technology Stack**

- **Backend**: Python Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: SQLite (Default Django database, can be migrated to other databases like PostgreSQL or MySQL)  
- **Admin Panel Enhancements**: Custom admin dashboards and inlines for efficient management.  

---

## **Installation Guide**

### **Prerequisites**
- Python 3.8 or higher  
- Django 4.x  
- Virtual environment (recommended)  

### **Steps**  
1. **Clone the repository**  
   ```bash
   git clone <repository_url>
   cd university-management
   ```  
2. **Set up the virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```  
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```  
4. **Apply database migrations**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```  
5. **Create a superuser**  
   ```bash
   python manage.py createsuperuser
   ```  
6. **Run the server**  
   ```bash
   python manage.py runserver
   ```  
7. Access the application at `http://127.0.0.1:8000/`.  

---

## **Usage**

### **User Roles**  
- **Admin**:  
  - Manage centers, departments, courses, and users.  
  - Approve/reject faculty verification requests.  

- **HOD (Head of Department)**:  
  - Assign faculty members to departments.  
  - Manage department-related subjects and courses.  

- **Faculty**:  
  - Track student attendance.  
  - Update internal marks and generate mark lists.  

### **Key URLs**  
- **Landing Page**: `/`  
- **Login**: `/login/`  
- **Signup**: `/signup/`  
- **About Page**: `/about/`  

---

## **System Design**

### **Database Models**  
- **User**: Extends `AbstractUser` with roles and verification status.  
- **Faculty**: Stores faculty details, linked to a `User`.  
- **Center**: Represents a university center.  
- **Department**: Belongs to a center and manages related courses and subjects.  
- **Course**: Assigned to departments, with related subjects.  
- **Student**: Tracks student data, attendance, and fee details.  
- **Subject**: Linked to departments and courses by semester.  
- **Fee**: Tracks semester and exam fees for students.  
- **MarkList**: Represents students' academic records.  
- **Tc**: Transfer certificate details.  
- **InternalMark**: Stores marks obtained by students for specific subjects.  
- **Attendance**: Tracks student attendance, including percentage calculation.  

### **Admin Customizations**  
- Inline models for related entities (e.g., Subjects in Courses, Departments in Centers).  
- Filters, search fields, and custom validation for better usability.  

---


## **Future Enhancements**

- Add APIs for mobile app integration.  
- Improve UI/UX for better usability.  
- Enable bulk uploads for student and course data.  
- Introduce notification and email alert systems.  

---

