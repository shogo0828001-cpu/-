from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import hashlib
import os
from pathlib import Path

# Database setup
DATABASE_URL = "sqlite:///./freelance.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================================
# Database Models
# ============================================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    user_type = Column(String)  # "engineer" or "company"
    created_at = Column(DateTime, default=datetime.utcnow)

    engineer = relationship("Engineer", back_populates="user", uselist=False)
    company = relationship("Company", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")


class Engineer(Base):
    __tablename__ = "engineers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String)
    bio = Column(Text)
    hourly_rate = Column(Float)
    experience_years = Column(Integer)
    skills = Column(String)
    portfolio_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    total_projects = Column(Integer, default=0)
    available = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="engineer")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    company_name = Column(String)
    industry = Column(String)
    website = Column(String, nullable=True)
    description = Column(Text)
    employee_count = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="company")
    jobs = relationship("Job", back_populates="company")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String)
    description = Column(Text)
    required_skills = Column(String)
    budget = Column(Float)
    duration = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String, default="pending")
    proposed_rate = Column(Float, nullable=True)
    cover_letter = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")


# Create tables
Base.metadata.create_all(bind=engine)

# ============================================================================
# Pydantic Models
# ============================================================================

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    user_type: str


class UserLogin(BaseModel):
    email: str
    password: str


class EngineerProfile(BaseModel):
    full_name: str
    bio: str
    hourly_rate: float
    experience_years: int
    skills: str
    portfolio_url: str = None
    github_url: str = None


class CompanyProfile(BaseModel):
    company_name: str
    industry: str
    website: str = None
    description: str
    employee_count: str = None


class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: str
    budget: float
    duration: str


class ApplicationCreate(BaseModel):
    job_id: int
    proposed_rate: float = None
    cover_letter: str


# ============================================================================
# Utilities
# ============================================================================

def hash_password(password: str) -> str:
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hash_value: str) -> bool:
    """Verify password"""
    return hash_password(password) == hash_value


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(title="フリーランスエンジニア集客プラットフォーム")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# API Routes
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """ホームページ"""
    return get_home_page()


@app.post("/api/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """新規登録"""
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています")

    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="このユーザー名は既に使用されています")

    password_hash = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=password_hash,
        user_type=user_data.user_type
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "登録成功しました",
        "user_id": user.id,
        "user_type": user.user_type,
        "username": user.username
    }


@app.post("/api/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """ログイン"""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="メールアドレスまたはパスワードが間違っています")

    return {
        "message": "ログイン成功しました",
        "user_id": user.id,
        "user_type": user.user_type,
        "username": user.username
    }


@app.post("/api/engineer/profile")
async def create_engineer_profile(
    profile: EngineerProfile,
    user_id: int,
    db: Session = Depends(get_db)
):
    """エンジニアプロフィール作成"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.user_type != "engineer":
        raise HTTPException(status_code=403, detail="エンジニアのみ使用できます")

    engineer = Engineer(
        user_id=user.id,
        full_name=profile.full_name,
        bio=profile.bio,
        hourly_rate=profile.hourly_rate,
        experience_years=profile.experience_years,
        skills=profile.skills,
        portfolio_url=profile.portfolio_url,
        github_url=profile.github_url
    )
    db.add(engineer)
    db.commit()
    db.refresh(engineer)
    return {"message": "プロフィール作成成功", "engineer_id": engineer.id}


@app.post("/api/company/profile")
async def create_company_profile(
    profile: CompanyProfile,
    user_id: int,
    db: Session = Depends(get_db)
):
    """企業プロフィール作成"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.user_type != "company":
        raise HTTPException(status_code=403, detail="企業のみ使用できます")

    company = Company(
        user_id=user.id,
        company_name=profile.company_name,
        industry=profile.industry,
        website=profile.website,
        description=profile.description,
        employee_count=profile.employee_count
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return {"message": "企業プロフィール作成成功", "company_id": company.id}


@app.post("/api/jobs")
async def create_job(
    job: JobCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """案件投稿（企業向け）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.user_type != "company":
        raise HTTPException(status_code=403, detail="企業のみ案件投稿できます")

    company = db.query(Company).filter(Company.user_id == user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="企業プロフィールが見つかりません")

    new_job = Job(
        company_id=company.id,
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        budget=job.budget,
        duration=job.duration
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "案件投稿成功", "job_id": new_job.id}


@app.get("/api/jobs")
async def list_jobs(db: Session = Depends(get_db)):
    """案件一覧取得"""
    jobs = db.query(Job).filter(Job.status == "active").all()
    return [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "required_skills": job.required_skills,
            "budget": job.budget,
            "duration": job.duration,
            "company_id": job.company_id,
            "created_at": job.created_at
        }
        for job in jobs
    ]


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """案件詳細取得"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="案件が見つかりません")

    company = db.query(Company).filter(Company.id == job.company_id).first()
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "required_skills": job.required_skills,
        "budget": job.budget,
        "duration": job.duration,
        "company": {
            "id": company.id,
            "name": company.company_name,
            "industry": company.industry
        } if company else None,
        "created_at": job.created_at
    }


@app.post("/api/applications")
async def create_application(
    app_data: ApplicationCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """案件に応募"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.user_type != "engineer":
        raise HTTPException(status_code=403, detail="エンジニアのみ応募できます")

    job = db.query(Job).filter(Job.id == app_data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="案件が見つかりません")

    existing = db.query(Application).filter(
        Application.user_id == user.id,
        Application.job_id == app_data.job_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="既に応募しています")

    application = Application(
        user_id=user.id,
        job_id=app_data.job_id,
        proposed_rate=app_data.proposed_rate,
        cover_letter=app_data.cover_letter
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return {"message": "応募成功しました", "application_id": application.id}


@app.get("/api/engineers")
async def list_engineers(db: Session = Depends(get_db)):
    """エンジニア一覧取得"""
    engineers = db.query(Engineer).filter(Engineer.available == True).all()
    return [
        {
            "id": eng.id,
            "full_name": eng.full_name,
            "hourly_rate": eng.hourly_rate,
            "experience_years": eng.experience_years,
            "skills": eng.skills,
            "rating": eng.rating,
            "total_projects": eng.total_projects,
            "portfolio_url": eng.portfolio_url,
            "github_url": eng.github_url
        }
        for eng in engineers
    ]


@app.get("/api/engineers/{engineer_id}")
async def get_engineer(engineer_id: int, db: Session = Depends(get_db)):
    """エンジニア詳細取得"""
    engineer = db.query(Engineer).filter(Engineer.id == engineer_id).first()
    if not engineer:
        raise HTTPException(status_code=404, detail="エンジニアが見つかりません")

    user = engineer.user
    return {
        "id": engineer.id,
        "full_name": engineer.full_name,
        "bio": engineer.bio,
        "hourly_rate": engineer.hourly_rate,
        "experience_years": engineer.experience_years,
        "skills": engineer.skills,
        "rating": engineer.rating,
        "total_projects": engineer.total_projects,
        "portfolio_url": engineer.portfolio_url,
        "github_url": engineer.github_url,
        "user_email": user.email if user else None
    }


# ============================================================================
# Static HTML Pages
# ============================================================================

def get_home_page():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>フリーランスエンジニア集客プラットフォーム</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f8f9fa;
            }

            header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem 2rem;
                position: sticky;
                top: 0;
                z-index: 100;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }

            header nav {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            header h1 {
                font-size: 1.8rem;
                font-weight: 700;
            }

            header nav a {
                color: white;
                text-decoration: none;
                margin: 0 1rem;
                cursor: pointer;
                transition: opacity 0.3s;
            }

            header nav a:hover {
                opacity: 0.8;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
            }

            .hero {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 4rem 2rem;
                text-align: center;
                margin: 2rem 0;
                border-radius: 10px;
            }

            .hero h2 {
                font-size: 2.5rem;
                margin-bottom: 1rem;
            }

            .hero p {
                font-size: 1.2rem;
                margin-bottom: 2rem;
                opacity: 0.9;
            }

            .btn-group {
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
            }

            .btn {
                padding: 0.8rem 2rem;
                border: none;
                border-radius: 5px;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
            }

            .btn-primary {
                background: #667eea;
                color: white;
            }

            .btn-primary:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            .btn-secondary {
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
            }

            .btn-secondary:hover {
                background: #f0f0f0;
            }

            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin: 3rem 0;
            }

            .feature-card {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                transition: transform 0.3s;
            }

            .feature-card:hover {
                transform: translateY(-5px);
            }

            .feature-card h3 {
                color: #667eea;
                margin-bottom: 1rem;
            }

            .job-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 1.5rem;
                margin: 2rem 0;
            }

            .job-card {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
            }

            .job-card h3 {
                margin-bottom: 0.5rem;
            }

            .job-badge {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                background: #e3f2fd;
                color: #667eea;
                border-radius: 20px;
                font-size: 0.85rem;
                margin: 0.25rem 0.25rem 0.25rem 0;
            }

            .auth-section {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                max-width: 400px;
                margin: 2rem auto;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }

            .form-group {
                margin-bottom: 1rem;
            }

            label {
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 500;
            }

            input, select {
                width: 100%;
                padding: 0.75rem;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 1rem;
            }

            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .toggle-panel {
                text-align: center;
                margin-top: 1rem;
                padding-top: 1rem;
                border-top: 1px solid #ddd;
            }

            .toggle-panel a {
                color: #667eea;
                cursor: pointer;
                text-decoration: none;
            }

            .toggle-panel a:hover {
                text-decoration: underline;
            }

            .hidden {
                display: none;
            }

            footer {
                background: #333;
                color: white;
                text-align: center;
                padding: 2rem;
                margin-top: 3rem;
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <h1>🚀 フリエン</h1>
                <div>
                    <a onclick="showHome()">ホーム</a>
                    <a onclick="showJobs()">案件一覧</a>
                    <a onclick="showEngineers()">エンジニア検索</a>
                    <a onclick="showAuth('login')">ログイン</a>
                </div>
            </nav>
        </header>

        <div class="container">
            <div id="home-section">
                <div class="hero">
                    <h2>フリーランスエンジニアと企業をつなぐプラットフォーム</h2>
                    <p>プロフェッショナルなエンジニアと優れたプロジェクトが出会う場所</p>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="showAuth('register')">無料登録</button>
                        <button class="btn btn-secondary" onclick="showJobs()">案件を探す</button>
                    </div>
                </div>

                <div class="features">
                    <div class="feature-card">
                        <h3>💼 企業向け</h3>
                        <p>優秀なフリーランスエンジニアを簡単に見つけて、プロジェクトを進めることができます。</p>
                    </div>
                    <div class="feature-card">
                        <h3>👨‍💻 エンジニア向け</h3>
                        <p>自分のスキルに合った案件を探して、自由に仕事を選ぶことができます。</p>
                    </div>
                    <div class="feature-card">
                        <h3>🤝 マッチング</h3>
                        <p>スキルと案件の最適なマッチングで、両者の成功を支援します。</p>
                    </div>
                </div>
            </div>

            <div id="jobs-section" class="hidden">
                <h2>最新の案件</h2>
                <div id="jobs-list" class="job-list"></div>
            </div>

            <div id="engineers-section" class="hidden">
                <h2>エンジニア検索</h2>
                <div id="engineers-list" class="job-list"></div>
            </div>

            <div id="auth-section" class="hidden">
                <div class="auth-section">
                    <div id="login-panel">
                        <h2>ログイン</h2>
                        <form onsubmit="handleLogin(event)">
                            <div class="form-group">
                                <label>メールアドレス</label>
                                <input type="email" id="login-email" required>
                            </div>
                            <div class="form-group">
                                <label>パスワード</label>
                                <input type="password" id="login-password" required>
                            </div>
                            <button class="btn btn-primary" style="width: 100%;">ログイン</button>
                        </form>
                        <div class="toggle-panel">
                            新規会員の方は <a onclick="toggleAuthPanel()">こちら</a>
                        </div>
                    </div>

                    <div id="register-panel" class="hidden">
                        <h2>新規登録</h2>
                        <form onsubmit="handleRegister(event)">
                            <div class="form-group">
                                <label>ユーザーネーム</label>
                                <input type="text" id="register-username" required>
                            </div>
                            <div class="form-group">
                                <label>メールアドレス</label>
                                <input type="email" id="register-email" required>
                            </div>
                            <div class="form-group">
                                <label>パスワード</label>
                                <input type="password" id="register-password" required>
                            </div>
                            <div class="form-group">
                                <label>ユーザータイプ</label>
                                <select id="register-type" required>
                                    <option value="">選択してください</option>
                                    <option value="engineer">エンジニア</option>
                                    <option value="company">企業</option>
                                </select>
                            </div>
                            <button class="btn btn-primary" style="width: 100%;">登録</button>
                        </form>
                        <div class="toggle-panel">
                            既にアカウントをお持ちの方は <a onclick="toggleAuthPanel()">こちら</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>&copy; 2024 フリーランスエンジニア集客プラットフォーム. All rights reserved.</p>
        </footer>

        <script>
            let currentUserId = localStorage.getItem('userId');
            let currentUserType = localStorage.getItem('userType');

            function showHome() {
                document.getElementById('home-section').classList.remove('hidden');
                document.getElementById('jobs-section').classList.add('hidden');
                document.getElementById('engineers-section').classList.add('hidden');
                document.getElementById('auth-section').classList.add('hidden');
            }

            function showJobs() {
                document.getElementById('home-section').classList.add('hidden');
                document.getElementById('jobs-section').classList.remove('hidden');
                document.getElementById('engineers-section').classList.add('hidden');
                document.getElementById('auth-section').classList.add('hidden');
                loadJobs();
            }

            function showEngineers() {
                document.getElementById('home-section').classList.add('hidden');
                document.getElementById('jobs-section').classList.add('hidden');
                document.getElementById('engineers-section').classList.remove('hidden');
                document.getElementById('auth-section').classList.add('hidden');
                loadEngineers();
            }

            function showAuth(type) {
                document.getElementById('home-section').classList.add('hidden');
                document.getElementById('jobs-section').classList.add('hidden');
                document.getElementById('engineers-section').classList.add('hidden');
                document.getElementById('auth-section').classList.remove('hidden');

                if (type === 'login') {
                    document.getElementById('login-panel').classList.remove('hidden');
                    document.getElementById('register-panel').classList.add('hidden');
                } else {
                    document.getElementById('login-panel').classList.add('hidden');
                    document.getElementById('register-panel').classList.remove('hidden');
                }
            }

            function toggleAuthPanel() {
                document.getElementById('login-panel').classList.toggle('hidden');
                document.getElementById('register-panel').classList.toggle('hidden');
            }

            async function loadJobs() {
                try {
                    const response = await fetch('/api/jobs');
                    const jobs = await response.json();
                    const listDiv = document.getElementById('jobs-list');
                    listDiv.innerHTML = '';

                    if (jobs.length === 0) {
                        listDiv.innerHTML = '<p>案件はまだ投稿されていません。</p>';
                        return;
                    }

                    jobs.forEach(job => {
                        const card = document.createElement('div');
                        card.className = 'job-card';
                        card.innerHTML = `
                            <h3>${job.title}</h3>
                            <div>
                                <span class="job-badge">予算: ¥${Math.floor(job.budget).toLocaleString()}</span>
                                <span class="job-badge">${job.duration}</span>
                            </div>
                            <p>${job.description.substring(0, 100)}...</p>
                            <small>必須スキル: ${job.required_skills}</small>
                        `;
                        listDiv.appendChild(card);
                    });
                } catch (error) {
                    console.error('エラー:', error);
                }
            }

            async function loadEngineers() {
                try {
                    const response = await fetch('/api/engineers');
                    const engineers = await response.json();
                    const listDiv = document.getElementById('engineers-list');
                    listDiv.innerHTML = '';

                    if (engineers.length === 0) {
                        listDiv.innerHTML = '<p>エンジニアはまだ登録されていません。</p>';
                        return;
                    }

                    engineers.forEach(engineer => {
                        const card = document.createElement('div');
                        card.className = 'job-card';
                        card.innerHTML = `
                            <h3>${engineer.full_name}</h3>
                            <div>
                                <span class="job-badge">時給: ¥${Math.floor(engineer.hourly_rate).toLocaleString()}</span>
                                <span class="job-badge">経験: ${engineer.experience_years}年</span>
                            </div>
                            <p>スキル: ${engineer.skills}</p>
                            <small>⭐ ${engineer.rating.toFixed(1)} (${engineer.total_projects}件)</small>
                        `;
                        listDiv.appendChild(card);
                    });
                } catch (error) {
                    console.error('エラー:', error);
                }
            }

            async function handleLogin(event) {
                event.preventDefault();
                const email = document.getElementById('login-email').value;
                const password = document.getElementById('login-password').value;

                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        localStorage.setItem('userId', data.user_id);
                        localStorage.setItem('userType', data.user_type);
                        alert('ログインしました！');
                        showHome();
                    } else {
                        alert('ログインに失敗しました。');
                    }
                } catch (error) {
                    alert('エラーが発生しました。');
                }
            }

            async function handleRegister(event) {
                event.preventDefault();
                const username = document.getElementById('register-username').value;
                const email = document.getElementById('register-email').value;
                const password = document.getElementById('register-password').value;
                const user_type = document.getElementById('register-type').value;

                try {
                    const response = await fetch('/api/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, email, password, user_type })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        localStorage.setItem('userId', data.user_id);
                        localStorage.setItem('userType', data.user_type);
                        alert('登録成功しました！');
                        showHome();
                    } else {
                        const error = await response.json();
                        alert('登録に失敗しました: ' + error.detail);
                    }
                } catch (error) {
                    alert('エラーが発生しました。');
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
