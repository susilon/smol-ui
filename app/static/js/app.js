// Toast notifications
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const colors = {
        success: 'bg-emerald-600',
        error: 'bg-red-600',
        info: 'bg-blue-600',
        warning: 'bg-amber-600'
    };
    const toast = document.createElement('div');
    toast.className = `${colors[type] || colors.info} text-white px-4 py-2 rounded-lg shadow-lg text-sm font-medium transition-all transform translate-x-0`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = 'opacity 0.3s, transform 0.3s';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// API fetch with error handling
async function apiFetch(url, options = {}) {
    try {
        const res = await fetch(url, options);
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            const detail = data.detail || `HTTP ${res.status}`;
            showToast(detail, 'error');
            return null;
        }
        return data;
    } catch (e) {
        showToast('Network error: cannot reach server', 'error');
        return null;
    }
}

// Modal
function showModal(content) {
    document.getElementById('modal-content').innerHTML = content;
    document.getElementById('modal').classList.remove('hidden');
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
    document.getElementById('modal-overlay').classList.add('hidden');
}

// Proxy status check
async function checkProxyStatus() {
    const el = document.getElementById('proxy-status');
    try {
        const res = await fetch('/api/keys');
        if (res.ok) {
            el.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400"></span><span class="text-emerald-400">Connected</span>';
        } else {
            const data = await res.json().catch(() => ({}));
            const detail = data.detail || `HTTP ${res.status}`;
            el.innerHTML = `<span class="w-2 h-2 rounded-full bg-amber-400"></span><span class="text-amber-400" title="${detail}">Proxy error</span>`;
        }
    } catch {
        el.innerHTML = '<span class="w-2 h-2 rounded-full bg-red-400"></span><span class="text-red-400">Disconnected</span>';
    }
}

// Active nav link
function setActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const page = link.dataset.page;
        if (page === 'dashboard' && path === '/') {
            link.classList.add('bg-gray-800', 'text-white');
        } else if (page !== 'dashboard' && path.includes(page)) {
            link.classList.add('bg-gray-800', 'text-white');
        } else {
            link.classList.remove('bg-gray-800', 'text-white');
        }
    });
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    setActiveNav();
    checkProxyStatus();
    // Refresh proxy status every 30s
    setInterval(checkProxyStatus, 30000);
});
