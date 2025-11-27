import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor pentru a adauga CSRF token
api.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

// Functie helper pentru a obtine cookie-uri
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// API endpoints
export const authAPI = {
  login: async (username, password) => {
    try {
      // Obtine CSRF token
      await api.get('/csrf/');
      // Login - foloseste endpoint-ul custom JSON
      const response = await api.post('/login/', {
        username,
        password
      });
      return response;
    } catch (error) {
      throw error;
    }
  },

  logout: async () => {
    try {
      await api.post('/logout/');
    } catch (error) {
      throw error;
    }
  },

  checkAuth: async () => {
    try {
      const response = await api.get('/check-auth/');
      return response.status === 200;
    } catch (error) {
      return false;
    }
  }
};

export const manifestAPI = {
  search: async (searchParams) => {
    try {
      const params = new URLSearchParams();
      if (searchParams.container) {
        params.append('container', searchParams.container);
      }
      if (searchParams.numar_manifest) {
        params.append('numar_manifest', searchParams.numar_manifest);
      }
      if (searchParams.year) {
        params.append('year', searchParams.year);
      }

      const response = await api.get(`/manifests/search/?${params.toString()}`);
      // DRF pagination may return {count, next, previous, results}
      // Extract results array if paginated, otherwise return data as-is
      return response.data.results || response.data;
    } catch (error) {
      throw error;
    }
  },

  getAll: async (page = 1) => {
    try {
      const response = await api.get(`/manifests/?page=${page}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export const yearsAPI = {
  getAll: async () => {
    try {
      const response = await api.get('/years/');
      // DRF pagination returns {count, next, previous, results}
      // Extract just the results array
      return response.data.results || response.data;
    } catch (error) {
      throw error;
    }
  },

  getActive: async () => {
    try {
      const response = await api.get('/years/');
      // Handle paginated response
      const years = response.data.results || response.data;
      const activeYear = years.find(y => y.is_active);
      return activeYear || (years.length > 0 ? years[0] : null);
    } catch (error) {
      throw error;
    }
  }
};

export const latestManifestAPI = {
  get: async (year) => {
    try {
      const params = new URLSearchParams();
      if (year) {
        params.append('year', year);
      }
      const response = await api.get(`/latest-manifest/?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default api;
