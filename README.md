# Course Management System (Ders Takip Sistemi)

A comprehensive Django-based educational course management system designed for tracking courses, documents, and teacher information.

## 🚀 Project Overview

This Course Management System is a web-based application built with Django that helps educational institutions manage:
- **Course Registration & Tracking**
- **Document Management (ERP & PANO modules)**
- **Teacher Information Management**
- **Student Participation Tracking**
- **PDF & Excel Report Generation**

> **Note**: This repository contains a prototype/draft version of the system. The production version is being developed privately and includes additional features and security enhancements.

## 📋 Features

### Core Modules
- **ERP Module**: Enterprise resource planning for educational activities
- **PANO Module**: Document panel management system
- **Teacher Management**: Comprehensive teacher profiles and course assignments
- **Course Management**: Full course lifecycle management
- **Archive System**: Organized storage for completed courses and documents

### Key Functionalities
- ✅ Course creation, editing, and status management (Active/Archive/Cancelled)
- ✅ Document upload and version control
- ✅ Multi-format export (PDF, Excel, Word)
- ✅ Real-time deadline tracking and warnings
- ✅ User authentication and authorization
- ✅ Responsive web design
- ✅ File management with download capabilities
- ✅ Archive and restore functionality

## 🛠️ Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **File Processing**: Python libraries for PDF/Excel generation
- **Authentication**: Django's built-in authentication system

## 📁 Project Structure

```
ders_takip/
├── account/           # User authentication and management
├── courses/           # Course management module
├── pages/             # Main application pages (ERP, PANO, etc.)
├── teacher/           # Teacher management module
├── templates/         # HTML templates
├── static/           # CSS, JS, and static files
├── media/            # Uploaded files and documents
└── manage.py         # Django management script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 4.x
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone [repository-url]
cd ders-takip-paneli
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 📖 Usage Guide

### Main Modules

1. **ERP Module** (`/erp/`)
   - Manage educational activities and resources
   - Track document statuses and deadlines
   - Generate comprehensive reports

2. **PANO Module** (`/pano/`)
   - Document panel management
   - File upload and organization
   - Archive management

3. **Teacher Management** (`/teacher/`)
   - Add and edit teacher profiles
   - Assign courses to teachers
   - Generate teacher-specific reports

4. **Course Management** (`/courses/`)
   - Create and manage courses
   - Set deadlines and requirements
   - Track course progress

## 📊 Key Features in Detail

### Document Management
- Multiple file format support
- Version control for documents
- Bulk download with ZIP compression
- Automatic deadline tracking

### Reporting System
- PDF generation for official documents
- Excel export for data analysis
- Customizable report templates
- Archive summaries

### Status Management
- Real-time status updates
- Color-coded warning systems
- Automatic notifications for deadlines
- Archive and restoration capabilities

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
The system is configured to use SQLite for development. For production, update settings to use PostgreSQL or MySQL.

## 📝 Development Status

This is a **prototype version** of the Course Management System. The current repository showcases the core functionality and system architecture. 

**Future Development:**
- Enhanced security features
- Advanced reporting capabilities
- Mobile application support
- Integration with external educational platforms
- Real-time notifications
- Advanced user role management

The production version is being developed privately with additional enterprise features and security enhancements.

## 🤝 Contributing

This is a prototype project for demonstration purposes. The main development continues in a private repository.

## 📄 License

This project is for educational and demonstration purposes. Please contact the development team for licensing information regarding production use.

## 🐛 Known Issues

- Some UI elements may require browser refresh after certain operations
- File upload size limits are set for development environment
- Advanced filtering features are in development

## 📞 Support

For questions about this prototype or the full system capabilities, please contact the development team.

---

**Disclaimer**: This repository contains a draft/prototype version of the system. The production version includes additional features, security enhancements, and optimizations that are not present in this public repository.