document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("streamSetupForm");
  const streamKeyInput = document.getElementById("streamKey");
  const connectionStatus = document.getElementById("connectionStatus");
  const startStreamBtn = document.getElementById("startStreamBtn");

  async function checkOBSConnection(streamKey) {
    connectionStatus.textContent = 'Đang kiểm tra kết nối...';
    connectionStatus.className = 'status connecting';
    startStreamBtn.disabled = true;

    try {
      const res = await fetch(`/api/check_stream/?streamKey=${encodeURIComponent(streamKey)}`, { method: 'GET' });
      if (!res.ok) throw new Error(`HTTP status ${res.status}`);
      const data = await res.json();

      if (data.status === 'connected') {
        connectionStatus.textContent = 'Kết nối thành công!';
        connectionStatus.className = 'status connected';
        startStreamBtn.disabled = false;
        return true;
      } else {
        connectionStatus.textContent = data.detail || 'Không tìm thấy kết nối từ phần mềm stream.';
        connectionStatus.className = 'status error';
        startStreamBtn.disabled = true;
        return false;
      }
    } catch (err) {
      connectionStatus.textContent = 'Lỗi kết nối với server: ' + err.message;
      connectionStatus.className = 'status error';
      startStreamBtn.disabled = true;
      return false;
    }
  }

  // Kiểm tra kết nối lần đầu
  const streamKey = streamKeyInput.value;
  if (streamKey) {
    checkOBSConnection(streamKey);
  } else {
    connectionStatus.textContent = 'Lỗi: Stream key không hợp lệ';
    connectionStatus.className = 'status error';
  }

  // Kiểm tra kết nối mỗi 5 giây
  setInterval(() => {
    if (streamKeyInput.value) {
      checkOBSConnection(streamKeyInput.value);
    }
  }, 5000);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const streamTitle = form.streamTitle.value.trim();
    const streamKey = streamKeyInput.value;

    if (!streamTitle) {
      alert("Vui lòng nhập tiêu đề livestream");
      return;
    }

    if (!streamKey) {
      alert("Stream key không hợp lệ");
      return;
    }

    const isConnected = await checkOBSConnection(streamKey);
    if (!isConnected) {
      alert("Không thể bắt đầu stream: kết nối với OBS/RTMP server thất bại.");
      return;
    }

    const url = new URL(window.location.origin + "/livestream/");
    url.searchParams.append("streamKey", streamKey);
    url.searchParams.append("title", streamTitle);
    window.location.href = url.toString();
  });
});