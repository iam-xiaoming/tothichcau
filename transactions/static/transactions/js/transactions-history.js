document.addEventListener("DOMContentLoaded", () => {
    const selectBtn = document.getElementById("statusFilter");
    const rows = document.querySelectorAll(".transaction-row");
    const refreshBtn = document.getElementById('refreshButton');
    const searchInput = document.getElementById("searchInput");

    function filterRowsByStatus(status) {
        rows.forEach(row => {
            const rowStatus = row.dataset.status;

            if (!status || status === rowStatus) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    refreshBtn.addEventListener('click', () => {
        selectBtn.value = "";
        filterRowsByStatus("");
    })

    selectBtn.addEventListener("change", () => {
        const selectedStatus = selectBtn.value;
        filterRowsByStatus(selectedStatus)
    });

    searchInput.addEventListener("input", async () => {
        let keyword = searchInput.value.trim();
        if (keyword.length > 0 && keyword.length < 2) return;

        if (!keyword) {
            keyword = "all";
        }

        try {
            const response = await fetch(`/api/search/transactions-history/?query=${keyword}&limit=20&offset=0`);
            if (!response.ok) {
                throw new Error("Failed to search transactions");
            }
            const data = await response.json();
            renderTransactions(data);
        } catch (error) {
            console.error("Search error:", error);
        }
    });

    function renderTransactions(transactions) {
        // Clear all current rows
        document.querySelectorAll(".transaction-row").forEach(row => row.remove());

        const tbody = document.querySelector("tbody");

        transactions.forEach(tx => {
            const tr = document.createElement("tr");
            const createdAt = tx.created_at
                ? new Date(tx.created_at).toLocaleString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                }) : '';
            tr.className = "transaction-row";
            tr.dataset.status = tx.status;
            tr.dataset.game = tx.game_name || tx.dlc_name || "";
            tr.innerHTML = `
                <td class="transaction-id"><code>${tx.id}</code></td>
                <td class="time-cell"><div class="time-info"><span class="datetime">${createdAt}</span></div></td>
                <td class="game-cell"><div class="game-info"><span class="game-name">${tx.game_name || tx.dlc_name || 'Unknown'}</span></div></td>
                <td class="price-cell"><span class="price">${tx.total_amount || 0}$</span></td>
                <td class="status-cell"><span class="status ${tx.status}"><i class="fas fa-check-circle"></i> ${tx.status}</span></td>
                <td class="action-cell">
                    <button class="detail-btn" onclick="event.stopPropagation(); viewTransactionDetail('${tx.id}')">
                        <i class="fas fa-eye"></i> Detail
                    </button>
                </td>
            `;
            tr.onclick = () => viewTransactionDetail(tx.id);
            tbody.appendChild(tr);
        });

        // Filter lại theo status đang chọn
        filterRowsByStatus(selectBtn.value);
    }
});