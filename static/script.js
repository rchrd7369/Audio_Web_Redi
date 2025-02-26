document.addEventListener("DOMContentLoaded", () => {
    const formElement = document.querySelector("#form-container");

    // Mengecek jika elemen ditemukan
    if (formElement) {
        window.addEventListener("scroll", () => {
            const scrollPosition = window.scrollY;
            console.log("Scroll Position:", scrollPosition); // Menambahkan log untuk debugging
            if (scrollPosition > 300) {
                formElement.classList.remove("opacity-0");
                formElement.classList.add("opacity-100");
                formElement.classList.add("transition-opacity");
            } else {
                formElement.classList.remove("opacity-100");
                formElement.classList.add("opacity-0");
            }
        });
    } else {
        console.error("Form element tidak ditemukan.");
    }
});

// Fungsi utama untuk menampilkan waktu Indonesia
function displayTime() {
    // Fungsi untuk memperbarui waktu
    function updateClock() {
        // Mendapatkan waktu saat ini di zona waktu Indonesia (Asia/Jakarta)
        const options = {
            timeZone: "Asia/Jakarta",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true
        };

        const now = new Date().toLocaleString("en-US", options);
        document.getElementById("time").textContent = "Waktu Indonesia: " + now; // Menampilkan waktu pada elemen dengan id 'time'
    }

    // Memperbarui waktu setiap detik
    setInterval(updateClock, 1000);
}

// Menjalankan fungsi displayTime ketika halaman dimuat
document.addEventListener("DOMContentLoaded", displayTime);
