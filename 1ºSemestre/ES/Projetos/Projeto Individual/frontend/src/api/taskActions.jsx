import axios from "./index"

export const postAddTask = (data, credential) => {
    return axios.post("/task", data, { headers: { credential: credential }})
}

export const getTasks = (filter_by, sort_by, sort_order, credential) => {
    return axios.get(`/task?filter_by=${filter_by}&sort_by=${sort_by}&sort_order=${sort_order}`, { headers: { credential: credential }})
}

export const putUpdateTask = (data, credential) => {
    return axios.put("/task", data, { headers: { credential: credential }})   
}

export const deleteTask = (task_id, credential) => {
    return axios.delete(`/task?task_id=${task_id}`, { headers: { credential: credential }})
}

export const getCategories = (credential) => {
    return axios.get("/task/category", { headers: { credential: credential }})
}