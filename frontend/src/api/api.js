import axios from "axios"

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true
})

api.interceptors.request.use(config => {
    const token = localStorage.getItem("access_token")

    if (token) {
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})

api.interceptors.response.use(
    response => response,

    async error => {

        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {

            originalRequest._retry = true

            try {

                const refreshResponse = await axios.post(
                    "http://127.0.0.1:8000/auth/refresh",
                    {},
                    { withCredentials: true }
                )

                if (refreshResponse.data?.access_token) {
                    localStorage.setItem("access_token", refreshResponse.data.access_token)
                }

                return api(originalRequest)

            } catch (refreshError) {

                console.log("Refresh failed")
                localStorage.removeItem("access_token")
                window.location.href = "/login"

            }
        }

        return Promise.reject(error)
    }
)

export default api