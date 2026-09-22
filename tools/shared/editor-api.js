/**
 * GFL2 Editor Tools - Shared API Client & Server Detector
 * Provides unified health checking, static server detection, and safe fetch operations.
 */

export class EditorServerError extends Error {
  constructor(message, isStaticServer = false, status = null) {
    super(message);
    this.name = 'EditorServerError';
    this.isStaticServer = isStaticServer;
    this.status = status;
  }
}

/**
 * Checks if the backend server is a valid gfl2-editor-server with the required capability.
 * @param {string} [requiredCapability]
 * @returns {Promise<{ok: boolean, data?: object, error?: string, isStaticServer?: boolean}>}
 */
export async function checkEditorServer(requiredCapability = null) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 3500);

  try {
    const resp = await fetch('/api/health', {
      cache: 'no-store',
      signal: controller.signal,
      headers: { 'Accept': 'application/json' },
    });
    clearTimeout(timeoutId);

    const contentType = resp.headers.get('Content-Type') || '';
    if (!contentType.includes('application/json')) {
      return {
        ok: false,
        error: 'Nhận phản hồi không phải JSON từ server (có thể là static server).',
        isStaticServer: true,
      };
    }

    if (!resp.ok) {
      return {
        ok: false,
        error: `Server phản hồi mã lỗi HTTP ${resp.status}`,
        isStaticServer: resp.status === 404,
      };
    }

    const data = await resp.json();
    if (data.service !== 'gfl2-editor-server') {
      return {
        ok: false,
        error: `Service không khớp (nhận được: ${data.service || 'không rõ'})`,
        isStaticServer: false,
      };
    }

    if (requiredCapability && (!Array.isArray(data.capabilities) || !data.capabilities.includes(requiredCapability))) {
      return {
        ok: false,
        error: `Server thiếu capability bắt buộc: '${requiredCapability}'`,
        isStaticServer: false,
      };
    }

    return { ok: true, data };
  } catch (err) {
    clearTimeout(timeoutId);
    return {
      ok: false,
      error: err.name === 'AbortError' ? 'Quá thời gian kết nối server (timeout 3.5s)' : (err.message || 'Lỗi kết nối'),
      isStaticServer: false,
    };
  }
}

/**
 * Safely requests a JSON endpoint with proper error handling and static-server detection.
 * @param {string} path
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
export async function requestJson(path, options = {}) {
  const headers = Object.assign(
    {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    options.headers || {}
  );

  const controller = new AbortController();
  const timeoutMs = options.timeout || 15000;
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  let resp;
  try {
    resp = await fetch(path, {
      ...options,
      headers,
      signal: options.signal || controller.signal,
    });
  } catch (err) {
    clearTimeout(timeoutId);
    throw new EditorServerError(
      err.name === 'AbortError' ? `Request timeout (${timeoutMs / 1000}s)` : `Lỗi mạng: ${err.message}`
    );
  }
  clearTimeout(timeoutId);

  const contentType = resp.headers.get('Content-Type') || '';
  const isJson = contentType.includes('application/json');

  if (!isJson) {
    if (resp.status === 404 || resp.status === 501) {
      throw new EditorServerError(
        'Bạn đang mở tool bằng static server. Chạy ".venv\\Scripts\\python.exe tools\\start_editors.py" rồi mở URL 127.0.0.1 được in ra.',
        true,
        resp.status
      );
    }
    const text = await resp.text();
    throw new EditorServerError(`Server trả về định dạng không phải JSON (${resp.status}): ${text.slice(0, 100)}`, false, resp.status);
  }

  const payload = await resp.json();
  if (!resp.ok) {
    throw new EditorServerError(payload.error || `HTTP ${resp.status}`, false, resp.status);
  }
  return payload;
}

/**
 * Attaches a server warning banner to the page if server is disconnected or wrong server.
 * @param {HTMLElement|string} container
 * @param {string} requiredCapability
 * @param {Array<HTMLElement|string>} [disableOnFailure]
 */
export async function setupServerGate(container, requiredCapability = null, disableOnFailure = []) {
  const bannerEl = typeof container === 'string' ? document.getElementById(container) : container;
  const disableEls = disableOnFailure.map((el) => (typeof el === 'string' ? document.getElementById(el) : el)).filter(Boolean);

  const health = await checkEditorServer(requiredCapability);
  if (!health.ok) {
    if (bannerEl) {
      bannerEl.innerHTML = `
        <div style="background: rgba(248, 81, 73, 0.2); border: 1px solid #f85149; color: #ff7b72; padding: 12px 16px; border-radius: 8px; margin: 12px 0; font-size: 14px; line-height: 1.5;">
          <strong>⚠️ Cảnh báo kết nối:</strong> ${health.error}<br>
          ${health.isStaticServer ? 'Bạn đang chạy tool trên static server. Hãy mở terminal và chạy:' : 'Hãy khởi động lại Editor Server bằng lệnh:'}
          <div style="margin-top: 6px;"><code style="background: rgba(0,0,0,0.5); padding: 3px 6px; border-radius: 4px; font-family: monospace;">.venv\\Scripts\\python.exe tools\\start_editors.py</code></div>
        </div>
      `;
      bannerEl.hidden = false;
    }
    disableEls.forEach((el) => {
      el.disabled = true;
      el.title = 'Vô hiệu hóa do không có kết nối tới Editor Server';
    });
    return false;
  }

  if (bannerEl) {
    bannerEl.hidden = true;
  }
  return true;
}
