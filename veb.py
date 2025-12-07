from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import random
import os

app = FastAPI(title="Career Path Builder API")

#настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#данные
class CareerGoal(BaseModel):
    profession: str
    experience_level: str = "junior"

#профессии
PROFESSIONS = {
    "Frontend разработчик": {
        "description": "Создание красивых и функциональных веб-интерфейсов",
        "salary": "120-180k",
        "demand": "Очень высокий",
        "skills": ["HTML", "CSS", "JavaScript", "React", "TypeScript"],
        "courses": [
            {"name": "HTML/CSS основы", "platform": "Stepik", "hours": 30},
            {"name": "JavaScript для начинающих", "platform": "Яндекс.Практикум", "hours": 60},
            {"name": "React полный курс", "platform": "Udemy", "hours": 40},
        ],
        "roadmap": [
            {"month": 1, "topic": "HTML, CSS и основы вёрстки"},
            {"month": 2, "topic": "JavaScript, работа с DOM"},
            {"month": 3, "topic": "React, компоненты и состояние"},
            {"month": 4, "topic": "TypeScript, продвинутые техники"},
            {"month": 5, "topic": "Создание портфолио, поиск работы"},
        ]
    },
    "Python разработчик": {
        "description": "Разработка мощных приложений и бэкенда на Python",
        "salary": "130-200k",
        "demand": "Очень высокий",
        "skills": ["Python", "Django/FastAPI", "PostgreSQL", "Docker", "Git"],
        "courses": [
            {"name": "Python для начинающих", "platform": "Coursera", "hours": 40},
            {"name": "Django основы", "platform": "Stepik", "hours": 50},
            {"name": "Работа с БД", "platform": "Udemy", "hours": 35},
        ],
        "roadmap": [
            {"month": 1, "topic": "Основы Python, синтаксис"},
            {"month": 2, "topic": "ООП, функции, модули"},
            {"month": 3, "topic": "Django/FastAPI, создание API"},
            {"month": 4, "topic": "Базы данных, PostgreSQL"},
            {"month": 5, "topic": "Docker, деплой, портфолио"},
        ]
    },
    "Data Analyst": {
        "description": "Анализ данных и создание интеллектуальных отчётов",
        "salary": "100-160k",
        "demand": "Высокий",
        "skills": ["SQL", "Python", "Tableau", "Excel", "Статистика"],
        "courses": [
            {"name": "SQL для анализа", "platform": "Coursera", "hours": 35},
            {"name": "Python с pandas", "platform": "Stepik", "hours": 50},
            {"name": "Tableau визуализация", "platform": "Udemy", "hours": 25},
        ],
        "roadmap": [
            {"month": 1, "topic": "SQL запросы, работа с данными"},
            {"month": 2, "topic": "Python, pandas, numpy"},
            {"month": 3, "topic": "Статистика и анализ"},
            {"month": 4, "topic": "Tableau, Power BI"},
            {"month": 5, "topic": "Проекты анализа, поиск работы"},
        ]
    },
    "UX/UI дизайнер": {
        "description": "Создание прекрасного опыта для пользователей",
        "salary": "90-150k",
        "demand": "Средний",
        "skills": ["Figma", "Design thinking", "Prototyping", "User research", "CSS"],
        "courses": [
            {"name": "Основы UX/UI дизайна", "platform": "Skillshare", "hours": 25},
            {"name": "Figma для дизайнеров", "platform": "Udemy", "hours": 30},
            {"name": "User experience research", "platform": "Coursera", "hours": 20},
        ],
        "roadmap": [
            {"month": 1, "topic": "Основы дизайна, цвет, типография"},
            {"month": 2, "topic": "Figma, инструменты дизайна"},
            {"month": 3, "topic": "UX исследования, юзер тестирование"},
            {"month": 4, "topic": "Создание портфолио, кейс-стади"},
            {"month": 5, "topic": "Job search, интервью, оффер"},
        ]
    },
    "DevOps инженер": {
        "description": "Управление инфраструктурой и развёртыванием приложений",
        "salary": "150-250k",
        "demand": "Очень высокий",
        "skills": ["Docker", "Kubernetes", "Linux", "CI/CD", "AWS/Azure"],
        "courses": [
            {"name": "Linux основы", "platform": "Udemy", "hours": 40},
            {"name": "Docker и контейнеризация", "platform": "Stepik", "hours": 35},
            {"name": "Kubernetes", "platform": "Linux Academy", "hours": 50},
        ],
        "roadmap": [
            {"month": 1, "topic": "Linux, командная строка"},
            {"month": 2, "topic": "Docker, контейнеры"},
            {"month": 3, "topic": "Kubernetes, оркестрация"},
            {"month": 4, "topic": "CI/CD pipelines"},
            {"month": 5, "topic": "Cloud (AWS/Azure), портфолио"},
        ]
    },
    "QA Engineer": {
        "description": "Тестирование и обеспечение качества программного обеспечения",
        "salary": "80-140k",
        "demand": "Средний",
        "skills": ["Тестирование", "Selenium", "API testing", "SQL", "Bagtracking"],
        "courses": [
            {"name": "Основы QA тестирования", "platform": "Stepik", "hours": 30},
            {"name": "Selenium и автоматизация", "platform": "Udemy", "hours": 40},
            {"name": "API тестирование", "platform": "Coursera", "hours": 25},
        ],
        "roadmap": [
            {"month": 1, "topic": "Основы тестирования, методология"},
            {"month": 2, "topic": "Selenium, автоматизация"},
            {"month": 3, "topic": "API тестирование, Postman"},
            {"month": 4, "topic": "SQL для QA"},
            {"month": 5, "topic": "Портфолио проектов, поиск работы"},
        ]
    }
}

# API Endpoints
@app.get("/")
def read_root():
   
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    else:
        return {"message": "🌸 Путеводитель по профессиям 🌸", "file_path": file_path}

@app.get("/professions")
def get_professions():
    """Получить все профессии"""
    professions = []
    for name, data in PROFESSIONS.items():
        professions.append({
            "name": name,
            "description": data["description"],
            "salary": data["salary"],
            "demand": data["demand"]
        })
    return {"professions": professions}

@app.post("/roadmap")
def generate_roadmap(goal: CareerGoal):
    profession = goal.profession
    
    if profession not in PROFESSIONS:
        return {"error": f"Профессия '{profession}' не найдена"}
    
    prof_data = PROFESSIONS[profession]
    
   
    courses = prof_data["courses"]
    if goal.experience_level == "middle":
        courses = courses[1:] 
    elif goal.experience_level == "senior":
        courses = courses[2:]  
    
    return {
        "profession": profession,
        "experience_level": goal.experience_level,
        "description": prof_data["description"],
        "salary_range": prof_data["salary"],
        "market_demand": prof_data["demand"],
        "required_skills": prof_data["skills"],
        "recommended_courses": courses,
        "learning_roadmap": prof_data["roadmap"],
        "estimated_time_months": len(prof_data["roadmap"])
    }

@app.get("/skill/{skill_name}")
def check_skill(skill_name: str):
    """Проверить востребованность навыка"""
    demand_options = ["Очень высокий", "Высокий", "Средний"]
    
    return {
        "skill": skill_name,
        "market_demand": random.choice(demand_options),
        "job_openings": random.randint(100, 500),
        "average_salary": f"{random.randint(80, 250)}k руб",
        "trend": random.choice(["растет ↑", "стабилен →", "падает ↓"])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)