
from .models import Course, CourseFile,CourseFileVersion
from teacher.models import Teacher
from datetime import datetime

def get_default_sections():
    """Returns the default sections."""
    return [
        "Ders Belgesi",
        "Müdür Yardımcısı Onaylı Ders Belgesi",
        "Ödevler Belgesi",
        "Müdür Yardımcısı Onaylı Ödevler Belgesi",
        "Yapılmış Ödevler Belgesi",
        "Müdür Yardımcısı Onaylı Yapılmış Ödevler Belgesi",
        "Raporlar",
        "Müdür Yardımcısı Onaylı Raporlar",
        "Video",
        "Excel Dosya Yüklemesi",
        "Eksiklik Belirtme",
    ]

def get_course_details(course):
    """
    Returns the details of a course including the count of files in each category.

    Args:
        course (Course): The course object.

    Returns:
        dict: A dictionary with file categories as keys and their counts as values.
    """
    files_of_course = CourseFile.objects.filter(course=course)
    files = {}
    for file in files_of_course:
        try:
            files[file.category] += 1
        except KeyError:
            files[file.category] = 1
    return files

def get_course_with_documents(course):
    """
    Returns the course details along with its associated documents.

    Args:
        course (Course): The course object.

    Returns:
        dict: A dictionary containing course details and a list of documents.
    """
    documents = CourseFile.objects.filter(course=course)
    documents_data = []
    documents_statu_dict={}
    for document in documents:
        documents_statu_dict[document.statu_pano] = documents_statu_dict.get(course.statu_pano, 0) + 1
        documents_data.append(
                    {
                        "id": document.id,
                        "category": document.category,
                        "belge_adi": document.current_version.file.name if document.current_version and document.current_version.file else None,
                        "belge_url": document.current_version.file.url if document.current_version and document.current_version.file else None,
                        "is_uploaded": document.sisteme_giris_tarihi,
                        "uploaded_at": document.sisteme_giris_tarihi
                        ,
                        "dilekce_name": document.dilekce_name,
                        "dilekce_is_uploaded": document.dilekce_is_uploaded,
                        "start_date": document.start_date,
                        "end_date": document.end_date,
                        "type": document.type,
                        "statu_pano": document.statu_pano,
                        "statu_erp": document.statu_pano,
                        "etkinlik_no": document.etkinlik_no,
                        "etkinlik_adi": document.etkinlik_adi,
                        "kodu": document.kodu,
                        "etkinklik_tarihi": document.etkinklik_tarihi,
                        "etkinlik_aciklamasi": document.etkinlik_aciklamasi,
                        "ogretmen_adi": document.ogretmen_adi,
                        "sinif": document.sinif,
                        "sehir": document.sehir,
                        "katilanlar": document.katilimcilar,
                        "katilimci_sayisi": document.katilimci_sayisi,
                        "sisteme_giris_tarihi": document.sisteme_giris_tarihi,
                        "egitim_olusturma_tarihi": document.egitim_olusturma_tarihi,
                        "katilimci_kodu": document.katilimci_kodu,
                        "egitim_kayit_no_1": document.egitim_kayit_no_1,
                        "egitim_kayit_no_2": document.egitim_kayit_no_2,
                        "egitim_kayit_no_3": document.egitim_kayit_no_3,
                        "description": document.description,
                        "description_1": document.description_1,
                        "description_2": document.description_2,
                        "description_3": document.description_3,
                        "created_at": document.created_at,
                        "created_by": document.created_by.username if document.created_by else None,
                    })
        
    return {
        "id": course.id,
        "name": course.name,
        "statu_pano": course.statu_pano,
        "statu_erp": course.statu_pano,
        "description": course.description,
        "start_date": course.start_year,
        "end_date": course.end_year,
        "dilekce_required": course.dilekce_required,
        "created_at": course.created_at,
        "created_by": course.created_by.username if course.created_by else None,
        "documents": documents_data,
        "document_statu_dict": documents_statu_dict
        }

def get_teachers_with_courses_and_documents(teacher_id=None, course_id=None, status=None, page = None):
    """
    Returns a list of teachers with their courses and associated documents.

    Args:
        teacher (int, optional): The ID of a specific teacher to filter by. Defaults to None.
        status (str, optional): The status of the courses to filter by. Defaults to None.

    Returns:
        list: A list of dictionaries containing teacher details, their courses, and documents.
    """
    today = datetime.today().date()
    teachers_data = []
    if teacher_id:
        teachers = Teacher.objects.filter(id=teacher_id)
    else:
        teachers = Teacher.objects.all()
    for teacher in teachers:
        teacher_warning_counter = 0
        if course_id:
            courses = Course.objects.filter(id=course_id)
        else:
            courses = Course.objects.filter(teacher=teacher)
        courses_data = []
        course_statu_dict = {}
        for course in courses:
            course_warning_counter = 0
            if status:
                if page == "pano":
                    course_statu_dict[course.statu_pano] = course_statu_dict.get(course.statu_pano, 0) + 1
                elif page == "erp":
                    course_statu_dict[course.statu_pano] = course_statu_dict.get(course.statu_pano, 0) + 1
                    
            documents = CourseFile.objects.filter(course=course)
            documents_data = []
            document_statu_dict = {}
            for document in documents:
                if status:
                    if page == "pano":
                        document_statu_dict[document.statu_pano] = document_statu_dict.get(document.statu_pano, 0) + 1                

                        if document.statu_pano != status:
                            continue

                    elif page == "erp":
                        document_statu_dict[document.statu_pano] = document_statu_dict.get(document.statu_pano, 0) + 1                
                        if document.statu_pano != status:
                            continue
                        
                versions = CourseFileVersion.objects.filter(course_file=document).order_by('-uploaded_at')
                document_warning_message = None
                if document.uyari_date:
                    belge_id = versions[0].id if versions else None
                    print(belge_id)
                    if belge_id == None:
                        document_warning_message = "Yüklenme Tarihi Yaklaştı"
                        course_warning_counter += 1
                else:
                    document_warning_message = None
                    
                
                
                
                documents_data.append(
                    {
                        "id": document.id,
                        "category": document.category,
                        "belge_adi": versions[0].file.name if versions else None,    
                        "belge_url": versions[0].file.url if versions else None,
                        "versions": [{"id": version.id, 
                                      "file": version.file.name.replace("uploads/",""), 
                                      "uploaded_at": version.uploaded_at.strftime("%Y-%m-%dT%H:%M:%S"),
                                      "download_url": version.file.url.replace("/uploads/uploads/", "/uploads/")} for version in versions],
                        "dilekce_name": document.dilekce_name,
                        "dilekce_is_uploaded": document.dilekce_is_uploaded,
                        "start_date": document.start_date,
                        "end_date": document.end_date,
                        "type": document.type,
                        "statu_pano": document.statu_pano,
                        "statu_erp": document.statu_pano,
                        "etkinlik_no": document.etkinlik_no,
                        "etkinlik_adi": document.etkinlik_adi,
                        "kodu": document.kodu,
                        "etkinklik_tarihi": document.etkinklik_tarihi,
                        "etkinlik_aciklamasi": document.etkinlik_aciklamasi,
                        "ogretmen_adi": document.ogretmen_adi,
                        "sinif": document.sinif,
                        "sehir": document.sehir,
                        "katilanlar": document.katilimcilar,
                        "katilimci_sayisi": document.katilimci_sayisi,
                        "sisteme_giris_tarihi": document.sisteme_giris_tarihi,
                        "egitim_olusturma_tarihi": document.egitim_olusturma_tarihi,
                        "katilimci_kodu": document.katilimci_kodu,
                        "egitim_kayit_no_1": document.egitim_kayit_no_1,
                        "egitim_kayit_no_2": document.egitim_kayit_no_2,
                        "egitim_kayit_no_3": document.egitim_kayit_no_3,
                        "description": document.description,
                        "description_1": document.description_1,
                        "description_2": document.description_2,
                        "description_3": document.description_3,
                        "created_at": document.created_at,
                        "created_by": document.created_by.username if document.created_by else None,
                        "warning_message": document_warning_message   
                    })
            
            if len(documents_data)!=0:
                course_warning_message = None                
                if course_warning_counter > 0:
                    teacher_warning_counter += 1
                    course_warning_message = f"{course_warning_counter} döküman yüklenmesi gerekiyor"
            
                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "statu_pano": course.statu_pano,
                    "statu_erp": course.statu_pano,
                    "description": course.description,
                    "start_date": course.start_year,
                    "end_date": course.end_year,
                    "dilekce_required": course.dilekce_required,
                    "created_at": course.created_at,
                    "created_by": course.created_by.username if course.created_by else None,
                    "documents": documents_data,
                    "document_statu_dict": document_statu_dict,
                    "warning_message": course_warning_message
                })
        teacher_warning_message = None
        
        if len(courses_data)!=0:
            if teacher_warning_counter > 0:
                teacher_warning_message = f"{teacher_warning_counter} ders döküman yüklemeyi bekliyor"
            teachers_data.append({
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "title": teacher.title,
                "description": teacher.description,
                "telephone": teacher.telephone,
                "telephone2": teacher.telephone2,
                "mail": teacher.mail,
                "adress": teacher.adress,
                "created_at": teacher.created_at,
                "created_by": teacher.created_by.username if teacher.created_by else None,
                "courses": courses_data,
                "course_statu_dict": course_statu_dict,
                "warning_message": teacher_warning_message
            })

    return teachers_data

def get_warnings( status=None, page = None):
    today = datetime.today()
    teachers_data = []
    teachers = Teacher.objects.all()
    for teacher in teachers:
        teacher_warning_counter = 0
        courses = Course.objects.filter(teacher=teacher)
        courses_data = []
        course_statu_dict = {}
        for course in courses:
            course_warning_counter = 0
            if status:
                if page == "pano":
                    course_statu_dict[course.statu_pano] = course_statu_dict.get(course.statu_pano, 0) + 1
                elif page == "erp":
                    course_statu_dict[course.statu_pano] = course_statu_dict.get(course.statu_pano, 0) + 1
                    
            documents = CourseFile.objects.filter(course=course)
            documents_data = []
            document_statu_dict = {}
            for document in documents:
                if status:
                    if page == "pano":
                        document_statu_dict[document.statu_pano] = document_statu_dict.get(document.statu_pano, 0) + 1                

                        if document.statu_pano != status:
                            continue

                    elif page == "erp":
                        document_statu_dict[document.statu_pano] = document_statu_dict.get(document.statu_pano, 0) + 1                
                        if document.statu_pano != status:
                            continue
                
                try:
                    start_date = document.start_date
                    end_date = document.end_date
                    days_to_end = (end_date - today).days
                    days_from_start = (today - start_date).days
                    document_warning_message = None
                    if days_from_start < days_to_end and document.sisteme_giris_tarihi==False:
                        document_warning_message = "Yükleme kalan gün: " + str(days_to_end)
                        course_warning_counter += 1
                except:
                    document_warning_message = None
                    
                
                
                documents_data.append(
                    {
                        "id": document.id,
                        "category": document.category,
                        "belge_adi": document.current_version.file.name if document.current_version and document.current_version.file else None,    
                        "belge_url": document.current_version.file.url if document.current_version and document.current_version.file else None,
                        "is_uploaded": document.sisteme_giris_tarihi,
                        "uploaded_at": document.sisteme_giris_tarihi,
                        "dilekce_name": document.dilekce_name,
                        "dilekce_is_uploaded": document.dilekce_is_uploaded,
                        "start_date": document.start_date,
                        "end_date": document.end_date,
                        "type": document.type,
                        "statu_pano": document.statu_pano,
                        "statu_erp": document.statu_pano,
                        "etkinlik_no": document.etkinlik_no,
                        "etkinlik_adi": document.etkinlik_adi,
                        "kodu": document.kodu,
                        "etkinklik_tarihi": document.etkinklik_tarihi,
                        "etkinlik_aciklamasi": document.etkinlik_aciklamasi,
                        "ogretmen_adi": document.ogretmen_adi,
                        "sinif": document.sinif,
                        "sehir": document.sehir,
                        "katilanlar": document.katilimcilar,
                        "katilimci_sayisi": document.katilimci_sayisi,
                        "sisteme_giris_tarihi": document.sisteme_giris_tarihi,
                        "egitim_olusturma_tarihi": document.egitim_olusturma_tarihi,
                        "katilimci_kodu": document.katilimci_kodu,
                        "egitim_kayit_no_1": document.egitim_kayit_no_1,
                        "egitim_kayit_no_2": document.egitim_kayit_no_2,
                        "egitim_kayit_no_3": document.egitim_kayit_no_3,
                        "description": document.description,
                        "description_1": document.description_1,
                        "description_2": document.description_2,
                        "description_3": document.description_3,
                        "created_at": document.created_at,
                        "created_by": document.created_by.username if document.created_by else None,
                        "warning_message": document_warning_message   
                    })
            
            if len(documents_data)!=0:
                course_warning_message = None                
                if course_warning_counter > 0:
                    teacher_warning_counter += 1
                    course_warning_message = f"{course_warning_counter} döküman yüklenmeyi bekliyor"
            
                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "statu_pano": course.statu_pano,
                    "statu_erp": course.statu_pano,
                    "description": course.description,
                    "start_date": course.start_year,
                    "end_date": course.end_year,
                    "dilekce_required": course.dilekce_required,
                    "created_at": course.created_at,
                    "created_by": course.created_by.username if course.created_by else None,
                    "documents": documents_data,
                    "document_statu_dict": document_statu_dict,
                    "warning_message": course_warning_message
                })
        teacher_warning_message = None
        
        if len(courses_data)!=0:
            if teacher_warning_counter > 0:
                teacher_warning_message = f"{teacher_warning_counter} ders döküman yüklemeyi bekliyor"
            teachers_data.append({
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "title": teacher.title,
                "description": teacher.description,
                "telephone": teacher.telephone,
                "telephone2": teacher.telephone2,
                "mail": teacher.mail,
                "adress": teacher.adress,
                "created_at": teacher.created_at,
                "created_by": teacher.created_by.username if teacher.created_by else None,
                "courses": courses_data,
                "course_statu_dict": course_statu_dict,
                "warning_message": teacher_warning_message
            })

    return teachers_data