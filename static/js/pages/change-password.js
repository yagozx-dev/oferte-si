document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('change-password-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showProgress();

    const old_password = document.getElementById('old_password').value;
    const new_password = document.getElementById('new_password').value;
    const confirm_password = document.getElementById('confirm_password').value;

    document.getElementById('form-errors').style.display = 'none';
    document.getElementById('form-success').style.display = 'none';

    if (new_password.length < 8) {
      mdSnackbar('A nova senha deve ter no mínimo 8 caracteres', 'error');
      hideProgress();
      return;
    }

    if (new_password !== confirm_password) {
      mdSnackbar('Nova senha e confirmação não conferem', 'error');
      hideProgress();
      return;
    }

    try {
      await api.post('/api/auth/change-password/', {
        old_password,
        new_password,
        confirm_password,
      });

      const successEl = document.getElementById('form-success');
      successEl.textContent = 'Senha alterada com sucesso!';
      successEl.style.display = 'block';

      document.getElementById('old_password').value = '';
      document.getElementById('new_password').value = '';
      document.getElementById('confirm_password').value = '';

      mdSnackbar('Senha alterada com sucesso', 'success');
    } catch (err) {
      const errors = err.data;
      let msg = 'Erro ao alterar senha';
      if (typeof errors === 'object') {
        msg = Object.values(errors).flat().join('. ');
      } else if (typeof errors === 'string') {
        msg = errors;
      }

      const errorEl = document.getElementById('form-errors');
      errorEl.textContent = msg;
      errorEl.style.display = 'block';
      mdSnackbar(msg, 'error');
    } finally {
      hideProgress();
    }
  });
});
