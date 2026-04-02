from dataclasses import dataclass, field


@dataclass
class Settings:
    app_name: str = "Turma AEB API"
    app_description: str = "Sistema multi-agente da Agencia Espacial Brasileira"
    app_version: str = "3.0.0"
    allow_origins: list[str] = field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:4173",
            "http://127.0.0.1:4173",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "https://sagi-crab.vercel.app",
        ]
    )
    allow_origin_regex: str = r"https:\/\/.*\.vercel\.app"


settings = Settings()
