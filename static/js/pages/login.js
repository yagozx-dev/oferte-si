document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const errorEl = document.getElementById('login-error');
  const toggleBtn = document.getElementById('toggle-password');

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => mdTogglePassword('password'));
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorEl.style.display = 'none';
    showProgress();

    try {
      const data = await api.post('/api/auth/login/', {
        email: emailInput.value,
        password: passwordInput.value,
      });

      api.setTokens(data.access, data.refresh);
      api.setUser(data.user);

      if (data.user.theme_primary_color) {
        localStorage.setItem('theme_primary_color', data.user.theme_primary_color);
      }

      window.location.href = '/';
    } catch (err) {
      errorEl.textContent = err.data?.error || 'Erro ao fazer login';
      errorEl.style.display = 'block';
    } finally {
      hideProgress();
    }
  });
});
