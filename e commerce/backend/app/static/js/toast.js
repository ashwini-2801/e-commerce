// Toast Notification Utility

const Toast = {
    show(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }
        
        const toast = document.createElement('div');
        toast.className = `toast glass-panel ${type}`;
        
        // Add icons based on toast type
        let icon = '';
        if (type === 'success') icon = '✓';
        else if (type === 'error') icon = '✗';
        else if (type === 'warning') icon = '⚠';
        else if (type === 'info') icon = 'ℹ';
        
        toast.innerHTML = `
            <div class="toast-content" style="display:flex; align-items:center; gap:0.5rem;">
                <span style="font-weight:bold; font-size:1.1rem;">${icon}</span>
                <span>${message}</span>
            </div>
            <div class="toast-close">&times;</div>
        `;
        
        // Close click event
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        });
        
        container.appendChild(toast);
        
        // Auto-dismiss after 4 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'fadeOut 0.3s ease forwards';
                setTimeout(() => toast.remove(), 300);
            }
        }, 4000);
    },
    
    success(message) { this.show(message, 'success'); },
    error(message) { this.show(message, 'error'); },
    warning(message) { this.show(message, 'warning'); },
    info(message) { this.show(message, 'info'); }
};

window.Toast = Toast;
