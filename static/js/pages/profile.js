document.addEventListener('DOMContentLoaded', () => {
  applyMasks();
  carregarProfile();

  document.getElementById('profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showProgress();

    const data = {
      nome: document.getElementById('nome').value,
      telefone: document.getElementById('telefone').value,
    };

    try {
      await api.put('/api/auth/profile/', data);
      const user = api.getUser();
      if (user) {
        user.nome = data.nome;
        api.setUser(user);
      }
      mdSnackbar('Dados atualizados com sucesso', 'success');
    } catch (err) {
      mdSnackbar('Erro ao atualizar dados', 'error');
    } finally {
      hideProgress();
    }
  });
});

async function carregarProfile() {
  showProgress();
  try {
    const data = await api.get('/api/auth/profile/');
    document.getElementById('nome').value = data.nome || '';
    document.getElementById('cpf').value = data.cpf || '';
    document.getElementById('telefone').value = data.telefone || '';
    document.getElementById('email').value = data.email || '';
  } catch (err) {
    mdSnackbar('Erro ao carregar perfil', 'error');
  } finally {
    hideProgress();
  }
}
