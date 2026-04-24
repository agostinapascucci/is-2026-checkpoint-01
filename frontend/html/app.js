/**
 * TeamBoard — app.js
 * Consume GET /api/team desde el backend Flask y construye la tabla dinámicamente.
 */

const API_URL = 'http://localhost:5000/api/team';
const HEALTH_URL = 'http://localhost:5000/api/health';

const teamBody = document.getElementById('team-body');
const statusBar = document.getElementById('status-bar');
const statusTxt = document.getElementById('status-text');

/** Actualiza el indicador de estado del backend en el header. */
function setStatus(ok, message) {
    statusBar.className = ok ? 'ok' : 'error';
    statusTxt.textContent = message;
}

/** Devuelve el HTML de una fila de la tabla a partir de un objeto miembro. */
function buildRow(member, index) {
    const statusClass = (member.estado || '').toLowerCase() === 'up' ? 'up' : 'down';
    const statusLabel = statusClass === 'up' ? 'UP' : 'DOWN';

    return `
    <tr>
      <td>${index + 1}</td>
      <td class="name-cell">
        <strong>${escapeHtml(member.nombre)} ${escapeHtml(member.apellido)}</strong>
        <small>${escapeHtml(String(member.legajo))}</small>
      </td>
      <td><span class="feature-tag">${escapeHtml(member.feature)}</span></td>
      <td class="service-name">${escapeHtml(member.servicio)}</td>
      <td><span class="badge ${statusClass}">${statusLabel}</span></td>
    </tr>
  `;
}

/** Escapa caracteres HTML para evitar XSS al renderizar datos del servidor. */
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/** Muestra un mensaje de error en el cuerpo de la tabla. */
function showError(message) {
    teamBody.innerHTML = `
    <tr class="state-row">
      <td colspan="5">${escapeHtml(message)}</td>
    </tr>
  `;
}

/** Verifica el health del backend y actualiza el indicador. */
async function checkHealth() {
    try {
        const res = await fetch(HEALTH_URL, { signal: AbortSignal.timeout(4000) });
        if (res.ok) {
            setStatus(true, 'Backend conectado · /api/health OK');
        } else {
            setStatus(false, `Backend respondió ${res.status}`);
        }
    } catch {
        setStatus(false, 'Backend no disponible');
    }
}

/** Solicita los integrantes al backend y los renderiza en la tabla. */
async function loadTeam() {
    try {
        const res = await fetch(API_URL, { signal: AbortSignal.timeout(6000) });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }

        const members = await res.json();

        if (!Array.isArray(members) || members.length === 0) {
            showError('No se encontraron integrantes en la base de datos.');
            return;
        }

        teamBody.innerHTML = members.map(buildRow).join('');

    } catch (err) {
        const isNetworkError = err instanceof TypeError;
        const msg = isNetworkError
            ? 'No se pudo conectar con el backend. ¿Está corriendo docker compose up?'
            : `Error al cargar datos: ${err.message}`;
        showError(msg);
        setStatus(false, 'Error al conectar con el backend');
    }
}

/** Punto de entrada: primero health check, luego datos. */
async function init() {
    await checkHealth();
    await loadTeam();
}

init();
