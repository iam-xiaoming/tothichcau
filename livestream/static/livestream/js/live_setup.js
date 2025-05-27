document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("streamSetupForm");
  const streamKeyInput = document.getElementById("streamKey");
  const connectionStatus = document.getElementById("connectionStatus");
  const startStreamBtn = document.getElementById("startStreamBtn");

  // Tạo streamKey ngẫu nhiên 32 ký tự
  function generateStreamKey() {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    return Array.from({ length: 32 }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
  }

  // Lấy streamKey từ localStorage hoặc tạo mới và lưu lại
  let savedKey = localStorage.getItem("streamKey");
  if (!savedKey) {
    savedKey = generateStreamKey();
    localStorage.setItem("streamKey", savedKey);
  }
  streamKeyInput.value = savedKey;

  async function checkOBSConnection(streamKey) {
    connectionStatus.textContent = 'Đang kiểm tra kết nối...';
    connectionStatus.className = 'status connecting';
    startStreamBtn.disabled = true;

    try {
      const res = await fetch(`/api/check_stream/?streamKey=${streamKey}`, { method: 'GET' });
      if (!res.ok) throw new Error(`HTTP status ${res.status}`);
      const data = await res.json();

      if (data.status === 'connected') {
        connectionStatus.textContent = 'Kết nối thành công!';
        connectionStatus.className = 'status connected';
        startStreamBtn.disabled = false;
        return true;
      } else {
        connectionStatus.textContent = 'Không tìm thấy kết nối từ phần mềm stream.';
        connectionStatus.className = 'status error';
        startStreamBtn.disabled = true;
        return false;
      }
    } catch (err) {
      connectionStatus.textContent = 'Lỗi kết nối với server.';
      connectionStatus.className = 'status error';
      startStreamBtn.disabled = true;
      return false;
    }
  }

  // Kiểm tra kết nối lần đầu khi tải trang
  checkOBSConnection(savedKey);

  // Kiểm tra kết nối lại mỗi 5 giây
  setInterval(() => {
    const currentKey = streamKeyInput.value || generateStreamKey();
    streamKeyInput.value = currentKey; // đảm bảo input luôn có giá trị hợp lệ
    checkOBSConnection(currentKey);
  }, 5000);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const streamTitle = form.streamTitle.value.trim();

    if (!streamTitle) {
      alert("Vui lòng nhập tiêu đề livestream");
      return;
    }

    const isConnected = await checkOBSConnection(streamKeyInput.value);
    if (!isConnected) {
      alert("Không thể bắt đầu stream: kết nối với OBS/RTMP server thất bại.");
      return;
    }

    // Redirect tới trang livestream với param streamKey và title
    const url = new URL(window.location.origin + "/livestream/");
    url.searchParams.append("streamKey", streamKeyInput.value);
    url.searchParams.append("title", streamTitle);

    window.location.href = url.toString();
  });
});