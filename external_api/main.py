from fastapi import FastAPI


app = FastAPI(title="External Task Helper API", version="1.0.0")


TIPS = {
    "geral": "Organizar tarefas do dia",
    "trabalho": "Priorizar tarefas com maior impacto",
    "estudo": "Revisar conteúdos pendentes",
    "saude": "Planejar rotina de autocuidado",
}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tips")
def task_tip(category: str = "geral"):
    title = TIPS.get(category.lower(), TIPS["geral"])
    return {
        "category": category,
        "title": title,
    }
