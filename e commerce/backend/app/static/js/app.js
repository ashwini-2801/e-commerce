// Common Client-Side Application Core Logic

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initial State Load
    App.init();
});

const App = {
    user: null,
    
    async init() {
        // Highlight active navbar link
        this.highlightActiveLink();
        
        // Check session details
        await this.checkSession();
        
        // Initialize common event listeners
        this.setupEventListeners();
    },
    
    async checkSession() {
        const res = await API.get('/api/auth/me');
        const userNav = document.getElementById('user-nav-section');
        const cartBadge = document.getElementById('cart-badge');
        
        if (res.data && res.data.logged_in) {
            this.user = res.data.user;
            
            // Render user dropdown menus in navbar
            if (userNav) {
                userNav.innerHTML = `
                    <div class="user-menu">
                        <span class="user-trigger">
                            👤 ${this.user.username} <small>(${this.user.role})</small> ▾
                        </span>
                        <div class="user-dropdown glass-panel">
                            ${this.user.role === 'admin' ? '<a href="/admin" class="dropdown-item">⚙ Admin Dashboard</a>' : ''}
                            <a href="/orders" class="dropdown-item">📦 My Orders</a>
                            <a href="#" id="logout-btn" class="dropdown-item" style="color:var(--danger);">🚪 Logout</a>
                        </div>
                    </div>
                `;
                
                // Attach logout action listener
                document.getElementById('logout-btn').addEventListener('click', (e) => {
                    e.preventDefault();
                    this.logout();
                });
            }
            
            // Sync cart quantity
            await this.updateCartCount();
        } else {
            this.user = null;
            if (userNav) {
                userNav.innerHTML = `
                    <a href="/login" class="btn btn-secondary" style="padding:0.4rem 1rem; font-size:0.9rem;">Sign In</a>
                    <a href="/register" class="btn btn-primary" style="padding:0.4rem 1rem; font-size:0.9rem;">Sign Up</a>
                `;
            }
            if (cartBadge) {
                cartBadge.style.display = 'none';
            }
        }
        
        // Dispatch event that session check is done, so specific pages can act
        document.dispatchEvent(new CustomEvent('sessionLoaded', { detail: this.user }));
    },
    
    async updateCartCount() {
        if (!this.user) return;
        
        const res = await API.get('/api/cart');
        const badge = document.getElementById('cart-badge');
        
        if (res.data && res.data.items && badge) {
            const count = res.data.items.reduce((sum, item) => sum + item.quantity, 0);
            if (count > 0) {
                badge.innerText = count;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    },
    
    async logout() {
        const res = await API.post('/api/auth/logout');
        if (!res.error) {
            Toast.success('Logged out successfully');
            setTimeout(() => {
                window.location.href = '/login';
            }, 1000);
        } else {
            Toast.error('Logout failed');
        }
    },
    
    highlightActiveLink() {
        const path = window.location.pathname;
        const links = document.querySelectorAll('.nav-link');
        
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (href === path || (path.startsWith(href) && href !== '/')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    },
    
    setupEventListeners() {
        // Universal hooks can go here
    },
    
    // Helper: format prices uniformly
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    // Helper: get query params
    getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }
};

window.App = App;
