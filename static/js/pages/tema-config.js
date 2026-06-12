let selectedColor = '#6750A4';

document.addEventListener('DOMContentLoaded', () => {
  carregarTema();

  document.querySelectorAll('.color-grid__item').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.color-grid__item').forEach(b => b.classList.remove('color-grid__item--active'));
      btn.classList.add('color-grid__item--active');
      selectedColor = btn.dataset.color;
      document.getElementById('custom-color').value = selectedColor;
      previewTheme(selectedColor);
    });
  });

  document.getElementById('custom-color').addEventListener('input', (e) => {
    document.querySelectorAll('.color-grid__item').forEach(b => b.classList.remove('color-grid__item--active'));
    selectedColor = e.target.value;
    previewTheme(selectedColor);
  });

  document.getElementById('reset-theme').addEventListener('click', () => {
    selectedColor = '#6750A4';
    previewTheme(selectedColor);
    document.querySelectorAll('.color-grid__item').forEach(b => b.classList.remove('color-grid__item--active'));
    document.querySelector('.color-grid__item').classList.add('color-grid__item--active');
    document.getElementById('custom-color').value = '#6750A4';
  });

  document.getElementById('tema-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showProgress();

    try {
      await api.put('/api/configuracao/tema/', { theme_primary_color: selectedColor });
      localStorage.setItem('theme_primary_color', selectedColor);
      mdSnackbar('Tema salvo com sucesso', 'success');
    } catch (err) {
      mdSnackbar('Erro ao salvar tema', 'error');
    } finally {
      hideProgress();
    }
  });
});

async function carregarTema() {
  try {
    const data = await api.get('/api/configuracao/tema/');
    if (data && data.theme_primary_color) {
      selectedColor = data.theme_primary_color;
      document.getElementById('custom-color').value = selectedColor;
      document.querySelectorAll('.color-grid__item').forEach(b => {
        b.classList.toggle('color-grid__item--active', b.dataset.color === selectedColor);
      });
      previewTheme(selectedColor);
    }
  } catch (e) {}
}

function previewTheme(color) {
  applyTheme(color);
  const preview = document.getElementById('theme-preview');
  preview.style.setProperty('--md-sys-color-primary', color);
  preview.style.setProperty('--md-sys-color-primary-container', hexToRgb(color, 0.15));
  preview.style.setProperty('--md-sys-color-on-primary', getContrastColor(color));

  const contrast = document.getElementById('contrast-indicator');
  const onPrimary = getContrastColor(color);
  if (onPrimary === '#FFFFFF') {
    contrast.textContent = '✅ Contraste WCAG AA: texto branco sobre a cor escolhida';
    contrast.style.backgroundColor = '#E8F5E9';
    contrast.style.color = '#2E7D32';
  } else {
    contrast.textContent = '⚠️ Contraste baixo: considere uma cor mais escura';
    contrast.style.backgroundColor = '#FFF3E0';
    contrast.style.color = '#E65100';
  }
  contrast.style.display = 'block';
}
