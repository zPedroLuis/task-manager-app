import { useEffect, useState } from "react";

import api from "../services/api";

const initialTask = {
  title: "",
  description: "",
  completed: false,
  category: "",
};

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [users, setUsers] = useState([]);
  const [taskForm, setTaskForm] = useState(initialTask);
  const [categoryName, setCategoryName] = useState("");
  const [filterCompleted, setFilterCompleted] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [search, setSearch] = useState("");
  const [nextPage, setNextPage] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);

  const fetchCategories = async () => {
    const response = await api.get("/categories/");
    setCategories(response.data);
  };

  const fetchUsers = async () => {
    const response = await api.get("/auth/users/");
    setUsers(response.data);
  };

  const fetchTasks = async (url = "/tasks/") => {
    const params = {};
    if (filterCompleted !== "") params.completed = filterCompleted;
    if (filterCategory) params.category = filterCategory;
    if (search) params.search = search;

    const response = await api.get(url, { params });
    setTasks(response.data.results || []);
    setNextPage(response.data.next);
    setPreviousPage(response.data.previous);
  };

  useEffect(() => {
    fetchCategories();
    fetchUsers();
  }, []);

  useEffect(() => {
    fetchTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterCompleted, filterCategory]);

  const handleCreateTask = async (event) => {
    event.preventDefault();
    const payload = {
      ...taskForm,
      category: taskForm.category || null,
    };
    await api.post("/tasks/", payload);
    setTaskForm(initialTask);
    fetchTasks();
  };

  const toggleTask = async (task) => {
    await api.patch(`/tasks/${task.id}/`, { completed: !task.completed });
    fetchTasks();
  };

  const deleteTask = async (taskId) => {
    await api.delete(`/tasks/${taskId}/`);
    fetchTasks();
  };

  const shareTask = async (taskId, userId) => {
    if (!userId) return;
    const task = tasks.find((item) => item.id === taskId);
    const currentShared = task?.shared_with || [];
    const nextShared = Array.from(new Set([...currentShared, Number(userId)]));
    await api.patch(`/tasks/${taskId}/`, { shared_with: nextShared });
    fetchTasks();
  };

  const handleCreateCategory = async (event) => {
    event.preventDefault();
    if (!categoryName.trim()) return;
    await api.post("/categories/", { name: categoryName });
    setCategoryName("");
    fetchCategories();
  };

  const suggestTitle = async () => {
    const selectedCategory = categories.find((c) => `${c.id}` === `${taskForm.category}`);
    const categoryQuery = selectedCategory ? selectedCategory.name.toLowerCase() : "geral";
    const response = await api.get(`/integrations/suggested-task-title/?category=${categoryQuery}`);
    setTaskForm((current) => ({ ...current, title: response.data.suggested_title }));
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/login";
  };

  return (
    <main className="container">
      <header className="header">
        <h1>Task Manager</h1>
        <button onClick={logout}>Sair</button>
      </header>

      <section className="grid">
        <article className="card">
          <h2>Nova tarefa</h2>
          <form className="form" onSubmit={handleCreateTask}>
            <input
              placeholder="Título"
              value={taskForm.title}
              onChange={(e) => setTaskForm({ ...taskForm, title: e.target.value })}
              required
            />
            <textarea
              placeholder="Descrição"
              value={taskForm.description}
              onChange={(e) => setTaskForm({ ...taskForm, description: e.target.value })}
            />
            <select
              value={taskForm.category}
              onChange={(e) => setTaskForm({ ...taskForm, category: e.target.value })}
            >
              <option value="">Sem categoria</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
            <div className="row">
              <button type="button" onClick={suggestTitle}>
                Sugerir título (API externa)
              </button>
              <button type="submit">Criar</button>
            </div>
          </form>
        </article>

        <article className="card">
          <h2>Categorias</h2>
          <form className="row" onSubmit={handleCreateCategory}>
            <input
              placeholder="Nova categoria"
              value={categoryName}
              onChange={(e) => setCategoryName(e.target.value)}
            />
            <button type="submit">Adicionar</button>
          </form>
          <ul>
            {categories.map((category) => (
              <li key={category.id}>{category.name}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="card">
        <h2>Minhas tarefas</h2>
        <div className="filters">
          <input placeholder="Buscar" value={search} onChange={(e) => setSearch(e.target.value)} />
          <button onClick={() => fetchTasks()}>Filtrar</button>
          <select value={filterCompleted} onChange={(e) => setFilterCompleted(e.target.value)}>
            <option value="">Todos os status</option>
            <option value="true">Concluídas</option>
            <option value="false">Pendentes</option>
          </select>
          <select value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)}>
            <option value="">Todas categorias</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id} className="task-item">
              <div>
                <strong>{task.title}</strong>
                <p>{task.description}</p>
                <small>Status: {task.completed ? "Concluída" : "Pendente"}</small>
                {task.shared_with?.length > 0 && (
                  <small> · Compartilhada com {task.shared_with.length} usuário(s)</small>
                )}
              </div>
              <div className="row">
                <select defaultValue="" onChange={(e) => shareTask(task.id, e.target.value)}>
                  <option value="">Compartilhar com...</option>
                  {users.map((user) => (
                    <option key={user.id} value={user.id}>
                      {user.username}
                    </option>
                  ))}
                </select>
                <button onClick={() => toggleTask(task)}>
                  {task.completed ? "Reabrir" : "Concluir"}
                </button>
                <button onClick={() => deleteTask(task.id)}>Excluir</button>
              </div>
            </li>
          ))}
        </ul>

        <div className="row">
          <button onClick={() => previousPage && fetchTasks(previousPage)} disabled={!previousPage}>
            Anterior
          </button>
          <button onClick={() => nextPage && fetchTasks(nextPage)} disabled={!nextPage}>
            Próxima
          </button>
        </div>
      </section>
    </main>
  );
}
