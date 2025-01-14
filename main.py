

def parse_resume(text):
    # Extracting full name
    full_name = re.search(r"Имя: (.+)", text).group(1).strip()
    
    # Extracting phone number
    number = re.search(r"Телефон: ([+\d\s\-]+)", text).group(1).strip()
    
    # Extracting email
    email = re.search(r"Почта: (.+)", text).group(1).strip()
    
    # Extracting "about me" section
    about_me_match = re.search(r"Обо мне\s+(.+?)\s+next", text, re.DOTALL)
    about_me = about_me_match.group(1).strip() if about_me_match else ""
    
    # Extracting job experience
    jobs = []
    for job_match in re.finditer(r"Компания: (.+?)\s+Должность: (.+?)\s+Дата: (.+?) - (.+?)\s+Описание: (.+?)\s+next", text, re.DOTALL):
        jobs.append({
            "name_company": job_match.group(1).strip(),
            "job_title": job_match.group(2).strip(),
            "from_date": job_match.group(3).strip(),
            "to_date": job_match.group(4).strip(),
            "job_description": job_match.group(5).strip()
        })
    
    # Extracting education
    education_match = re.search(r"Университет: (.+?)\s+Направление: (.+?)\s+next", text, re.DOTALL)
    education = {
        "university": education_match.group(1).strip(),
        "major": education_match.group(2).strip()
    } if education_match else {}
    
    # Extracting skills
    skills_match = re.search(r"Навыки\s+- (.+)", text, re.DOTALL)
    skills = [skill.strip() for skill in skills_match.group(1).split("\n- ")] if skills_match else []
    
    # Compiling the result
    return {
        "full_name": full_name,
        "number": number,
        "email": email,
        "about_me": about_me,
        "jobs": jobs,
        "education": education,
        "skills": skills
    }

# Example usage
resume_text = """Контактная информация
Имя: Азамат Азаматов
Телефон: +998946654282
Почта: azamatovuser@gmail.com

next

Обо мне
Я — backend разработчик с опытом работы в создании надежных и масштабируемых серверных приложений. Имею опыт работы с технологиями, такими как Python, Django, FastAPI, Docker и CI/CD. Веду разработку с упором на качество кода и автоматизацию процессов.

next

Опыт работы
Компания: EPAM
Должность: Backend инженер
Дата: Октябрь 2023 - Сейчас
Описание: Отвечаю за разработку серверной части приложений, создание API эндпоинтов и настройку процессов контейнеризации с использованием Docker. Занимаюсь интеграцией CI/CD и обеспечением качества кода путем написания тестов.

next

Образование
Университет: INHA University
Направление: Экономика

next

Навыки
- Python
- Django
- FastAPI
- Docker
- CI/CD
- Nginx"""

parsed_data = parse_resume(resume_text)
print(parsed_data)
