document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 Script loaded successfully");

    let uploadForm = document.getElementById("uploadForm");
    let fileInput = document.getElementById("fileInput");
    let downloadExcelButton = document.getElementById("downloadexcel");
    let searchInput = document.getElementById("searchInput");

    if (uploadForm && fileInput) {
        uploadForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            if (fileInput.files.length === 0) {
                alert("🚨 Please select a file to upload!");
                return;
            }

            let formData = new FormData();
            formData.append("file", fileInput.files[0]);

            try {
                let response = await fetch("http://127.0.0.1:8080/upload", {
                    method: "POST",
                    body: formData
                });

                let data = await response.json();

                if (response.ok) {
                    alert("✅ File uploaded successfully!");
                    console.log("✅ Upload Success:", data);
                } else {
                    alert(`❌ Upload failed: ${data.error}`);
                    console.error("❌ Upload Error:", data);
                }
            } catch (error) {
                console.error("❌ Error uploading file:", error);
                alert("⚠️ An error occurred while uploading the file.");
            }
        });
    } else {
        console.error("🚨 Upload form or file input not found! Check your HTML.");
    }

    // ✅ Search input event listener
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            fetchData(this.value);
        });
    } else {
        console.error("❌ Search input not found!");
    }

    if (downloadExcelButton) {
        downloadExcelButton.addEventListener("click", function () {
            console.log("📥 Download button clicked");

            fetch("http://127.0.0.1:8080/download-excel")
                .then(response => response.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "rdlfiles.xlsx";
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => console.error("❌ Error downloading Excel file:", error));
        });
    } else {
        console.error("❌ Download Excel button not found!");
    }
});

// ✅ Ensure fetchData() is globally accessible
if (typeof fetchData === "undefined") {
    function fetchData(query = "") {
        console.log("Fetching data for query:", query);

        fetch(`http://127.0.0.1:8080/search?query=${query}`)
            .then(response => response.json())
            .then(data => {
                const tableHead = document.getElementById("table-head");
                const tableBody = document.getElementById("table-body");

                tableHead.innerHTML = "";
                tableBody.innerHTML = "";

                if (data.results && data.results.length > 0) {
                    const headers = Object.keys(data.results[0]);

                    headers.forEach(header => {
                        const th = document.createElement("th");
                        th.textContent = header;
                        tableHead.appendChild(th);
                    });

                    data.results.forEach(rowData => {
                        const row = document.createElement("tr");
                        headers.forEach(header => {
                            const td = document.createElement("td");
                            let cellContent = rowData[header] !== null ? rowData[header] : "";

                            if (header === headers[0]) {
                                let fullText = rowData[header];

                                // 💡 Strip only for the download URL
                                let cleanFilename = fullText.replace(/^\d+\s*-\s*/, "");

                                const rdlLink = document.createElement("a");
                                rdlLink.href = `http://127.0.0.1:8080/download/${encodeURIComponent(cleanFilename)}`;
                                rdlLink.textContent = fullText; // Show full name like "33 - Whatever"
                                rdlLink.setAttribute("download", cleanFilename);
                                rdlLink.target = "_blank";
                                td.appendChild(rdlLink);
                            } else {
                                td.textContent = cellContent;
                            }

                            row.appendChild(td);
                        });
                        tableBody.appendChild(row);
                    });
                } else {
                    tableBody.innerHTML = '<tr><td colspan="100%">No results found</td></tr>';
                }
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                document.getElementById("table-body").innerHTML = `<tr><td colspan="100%">An error occurred: ${error.message}</td></tr>`;
            });
    }

    window.fetchData = fetchData;
}
